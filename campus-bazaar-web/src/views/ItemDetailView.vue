<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { itemApi, orderApi, commentApi, reviewApi } from '../api/index'
import { useUserStore } from '../stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const item = ref(null)
const loading = ref(true)
const favLoading = ref(false)
const orderLoading = ref(false)

// 下单弹窗
const showOrderModal = ref(false)
const orderForm = ref({ message: '', meetPlace: '' })

const conditionMap = ['', '几乎全新', '轻微使用', '正常使用', '明显使用', '大量使用']
const statusMap = {
  0: { text: '待审核', cls: 'badge-gray' },
  1: { text: '在售', cls: 'badge-green' },
  2: { text: '锁定中', cls: 'badge-yellow' },
  3: { text: '已售出', cls: 'badge-gray' },
  4: { text: '已下架', cls: 'badge-red' }
}

const images = computed(() => {
  if (!item.value?.images) return []
  return item.value.images.split(',').filter(Boolean)
})
const activeImg = ref(0)

const isMine = computed(() => userStore.user?.id === item.value?.sellerId)
const canBuy = computed(() => item.value?.status === 1 && !isMine.value && userStore.isLoggedIn())

async function loadItem() {
  loading.value = true
  try {
    const res = await itemApi.getDetail(route.params.id)
    item.value = res.data
  } catch (e) {
    window.$toast?.(e.message, 'error')
  } finally {
    loading.value = false
  }
}

async function toggleFav() {
  if (!userStore.isLoggedIn()) { router.push('/login'); return }
  favLoading.value = true
  try {
    await itemApi.addFavorite(item.value.id)
    item.value.favCount++
    window.$toast?.('已收藏')
  } catch (e) {
    // 可能已收藏，尝试取消
    if (e.message.includes('已收藏')) {
      window.$toast?.(e.message, 'error')
    } else {
      window.$toast?.(e.message, 'error')
    }
  } finally {
    favLoading.value = false
  }
}

async function submitOrder() {
  if (!orderForm.value.meetPlace.trim()) {
    window.$toast?.('请填写交易地点', 'error'); return
  }
  orderLoading.value = true
  try {
    await orderApi.submit({
      itemId: item.value.id,
      message: orderForm.value.message,
      meetPlace: orderForm.value.meetPlace
    })
    window.$toast?.('下单成功，等待卖家确认')
    showOrderModal.value = false
    item.value.status = 2
  } catch (e) {
    window.$toast?.(e.message, 'error')
  } finally {
    orderLoading.value = false
  }
}

async function takeDown() {
  if (!confirm('确认下架该商品？')) return
  try {
    await itemApi.takeDown(item.value.id)
    window.$toast?.('商品已下架')
    item.value.status = 4
  } catch (e) {
    window.$toast?.(e.message, 'error')
  }
}

// ===== 留言/回复 =====
const comments = ref([])
const commentContent = ref('')
const replyTo = ref(null)
const replyContent = ref('')
const commentLoading = ref(false)

async function loadComments() {
  try {
    const res = await commentApi.listByItem(item.value.id)
    comments.value = res.data
  } catch { }
}

async function addComment() {
  if (!commentContent.value.trim()) return
  commentLoading.value = true
  try {
    await commentApi.add({ itemId: item.value.id, content: commentContent.value.trim() })
    commentContent.value = ''
    await loadComments()
  } catch (e) {
    window.$toast?.(e.message, 'error')
  }
  commentLoading.value = false
}

async function addReply(commentId) {
  if (!replyContent.value.trim()) return
  commentLoading.value = true
  try {
    await commentApi.reply(commentId, { content: replyContent.value.trim() })
    replyContent.value = ''
    replyTo.value = null
    await loadComments()
  } catch (e) {
    window.$toast?.(e.message, 'error')
  }
  commentLoading.value = false
}

// ===== 评价 =====
const review = ref(null)
const reviewScore = ref(0)
const reviewContent = ref('')
const reviewLoading = ref(false)

async function loadReview() {
  try {
    const res = await reviewApi.getByItem(item.value.id)
    review.value = res.data
  } catch { }
}

async function submitReview() {
  if (reviewScore.value === 0) {
    window.$toast?.('请选择评分', 'error'); return
  }
  reviewLoading.value = true
  try {
    // Find the order for this item that current user is the buyer
    const res = await reviewApi.create({
      orderId: userOrderId.value,
      score: reviewScore.value,
      content: reviewContent.value.trim()
    })
    review.value = res.data
    window.$toast?.('评价成功')
  } catch (e) {
    window.$toast?.(e.message, 'error')
  }
  reviewLoading.value = false
}

const userOrderId = ref(null)
const canReview = ref(false)

async function checkCanReview() {
  if (!userStore.isLoggedIn() || !isMine.value === false) return
  // Need to find the order relevant to this item and current buyer
  try {
    const buyOrders = await orderApi.getMyBuyOrders()
    const orders = buyOrders.data || []
    const order = orders.find(o => o.itemId === item.value.id && o.status === 2 && o.buyerId === userStore.user.id)
    if (order) {
      const checkRes = await reviewApi.checkCanReview(order.id)
      if (checkRes.data) {
        userOrderId.value = order.id
        canReview.value = true
      }
    }
  } catch { }
}

// ===== 锁定订单信息 =====
const lockOrder = ref(null)
const sellerConfirmLoading = ref(false)

async function loadLockOrder() {
  if (item.value.status !== 2 || !userStore.isLoggedIn()) return
  try {
    const res = await orderApi.getByItem(item.value.id)
    lockOrder.value = res.data
  } catch { }
}

async function sellerAgree() {
  if (!lockOrder.value) return
  sellerConfirmLoading.value = true
  try {
    await orderApi.confirm(lockOrder.value.id)
    window.$toast?.('已同意出售，等待买家确认完成')
    lockOrder.value.status = 1
    item.value.status = 2
  } catch (e) {
    window.$toast?.(e.message, 'error')
  }
  sellerConfirmLoading.value = false
}

const isBuyer = computed(() => {
  return lockOrder.value && userStore.user && lockOrder.value.buyerId === userStore.user.id
})

onMounted(() => { loadItem().then(() => { loadComments(); loadReview(); checkCanReview(); loadLockOrder() }) })
</script>

<template>
  <div class="container detail-page">
    <div v-if="loading" class="loading-wrap">加载中…</div>

    <template v-else-if="item">
      <!-- 面包屑 -->
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span> / </span>
        <span>{{ item.categoryName }}</span>
        <span> / </span>
        <span class="cur">{{ item.title }}</span>
      </div>

      <div class="detail-body">
        <!-- 左：图片区 -->
        <div class="img-section">
          <div class="main-img-wrap">
            <img v-if="images[activeImg]" :src="images[activeImg]" class="main-img" :alt="item.title" />
            <div v-else class="main-img-placeholder">📦</div>
            <span class="badge status-badge-lg" :class="statusMap[item.status]?.cls">
              {{ statusMap[item.status]?.text }}
            </span>
          </div>
          <div v-if="images.length > 1" class="thumb-list">
            <img
              v-for="(img, i) in images"
              :key="i"
              :src="img"
              class="thumb"
              :class="{ active: activeImg === i }"
              @click="activeImg = i"
            />
          </div>
        </div>

        <!-- 右：信息区 -->
        <div class="info-section">
          <h1 class="item-title">{{ item.title }}</h1>

          <div class="price-row">
            <span class="big-price">¥{{ item.price }}</span>
            <span v-if="item.originalPrice" class="ori-price">原价 ¥{{ item.originalPrice }}</span>
            <span v-if="item.originalPrice" class="discount">
              {{ Math.round(item.price / item.originalPrice * 10) }}折
            </span>
          </div>

          <div class="tag-row">
            <span class="badge badge-green">{{ conditionMap[item.conditionLevel] }}</span>
            <span class="badge badge-gray">{{ item.categoryName }}</span>
            <span class="stat-text">👁 {{ item.viewCount }} · ❤️ {{ item.favCount }}</span>
          </div>

          <!-- 卖家信息 -->
          <div class="seller-card">
            <div class="seller-avatar">{{ (item.sellerNickname || '?')[0] }}</div>
            <div class="seller-detail">
              <span class="seller-name">{{ item.sellerNickname }}</span>
              <router-link :to="`/seller/${item.sellerId}`" class="seller-link">查看Ta的其他商品 →</router-link>
            </div>
          </div>

          <!-- 描述 -->
          <div class="desc-section">
            <div class="section-label">商品描述</div>
            <p class="desc-text">{{ item.description || '卖家暂未填写描述' }}</p>
          </div>

          <!-- 发布时间 -->
          <div class="meta-row">
            <span>📅 发布于 {{ item.createdAt }}</span>
          </div>

          <!-- 操作按钮 -->
          <div class="action-row">
            <!-- 在售：正常买卖 -->
            <template v-if="item.status === 1">
              <template v-if="isMine">
                <router-link :to="`/edit/${item.id}`" class="btn btn-outline btn-lg">编辑商品</router-link>
                <button class="btn btn-ghost btn-lg" @click="takeDown">下架</button>
              </template>
              <template v-else>
                <button class="btn btn-primary btn-lg" :disabled="!canBuy" @click="showOrderModal = true">立即预购</button>
                <button class="btn btn-outline btn-lg" :disabled="favLoading" @click="toggleFav">❤️ 收藏</button>
              </template>
            </template>

            <!-- 锁定：卖家同意 / 买家等待 -->
            <template v-else-if="item.status === 2">
              <template v-if="isMine">
                <button class="btn btn-success btn-lg" :disabled="sellerConfirmLoading" @click="sellerAgree">
                  {{ sellerConfirmLoading ? '处理中…' : '同意出售' }}
                </button>
                <router-link :to="`/edit/${item.id}`" class="btn btn-outline btn-lg">编辑商品</router-link>
              </template>
              <template v-else-if="isBuyer">
                <span class="lock-status-text">⏳ 等待卖家确认中…</span>
              </template>
              <template v-else>
                <span class="lock-status-text">已被预订</span>
              </template>
            </template>

            <!-- 已售 -->
            <template v-else-if="item.status === 3">
              <template v-if="isMine">
                <span class="sold-text">已售出</span>
              </template>
              <template v-else>
                <span class="sold-text">已售出</span>
              </template>
            </template>

            <!-- 待审核/下架 -->
            <template v-else>
              <template v-if="isMine">
                <router-link v-if="item.status === 0" :to="`/edit/${item.id}`" class="btn btn-outline btn-lg">编辑商品</router-link>
                <button v-if="item.status !== 4" class="btn btn-ghost btn-lg" @click="takeDown">下架</button>
              </template>
              <template v-else>
                <span class="lock-status-text">{{ statusMap[item.status]?.text }}</span>
              </template>
            </template>
          </div>

          <!-- 锁定：买家信息卡片（仅卖家可见） -->
          <div v-if="item.status === 2 && isMine && lockOrder" class="lock-info-card">
            <div class="lock-info-title">买家信息</div>
            <div class="lock-info-grid">
              <div class="lock-info-item">
                <span class="lock-info-label">买家昵称</span>
                <span class="lock-info-value">{{ lockOrder.buyerNickname }}</span>
              </div>
              <div v-if="lockOrder.buyerSchool" class="lock-info-item">
                <span class="lock-info-label">学校</span>
                <span class="lock-info-value">{{ lockOrder.buyerSchool }}</span>
              </div>
              <div class="lock-info-item">
                <span class="lock-info-label">交易地点</span>
                <span class="lock-info-value">{{ lockOrder.meetPlace || '未指定' }}</span>
              </div>
              <div class="lock-info-item">
                <span class="lock-info-label">下单时间</span>
                <span class="lock-info-value">{{ lockOrder.createdAt }}</span>
              </div>
            </div>
            <div v-if="lockOrder.message" class="lock-info-msg">
              <span class="lock-info-label">买家留言</span>
              <p>{{ lockOrder.message }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 留言交流区（状态：在售 / 锁定） -->
      <div v-if="item.status === 1 || item.status === 2" class="comment-section card">
        <h3 class="section-heading">交流区</h3>

        <!-- 留言列表 -->
        <div v-if="comments.length > 0" class="comment-list">
          <div v-for="c in comments" :key="c.id" class="comment-item">
            <div class="comment-avatar">{{ (c.userNickname || '?')[0] }}</div>
            <div class="comment-body">
              <div class="comment-head">
                <strong>{{ c.userNickname }}</strong>
                <span class="comment-time">{{ c.createdAt }}</span>
              </div>
              <p class="comment-text">{{ c.content }}</p>
              <button v-if="userStore.isLoggedIn()" class="reply-btn" @click="replyTo = replyTo === c.id ? null : c.id">回复</button>

              <!-- 回复列表 -->
              <div v-if="c.replies && c.replies.length > 0" class="reply-list">
                <div v-for="r in c.replies" :key="r.id" class="reply-item">
                  <div class="comment-avatar small">{{ (r.userNickname || '?')[0] }}</div>
                  <div class="comment-body">
                    <div class="comment-head">
                      <strong>{{ r.userNickname }}</strong>
                      <span class="comment-time">{{ r.createdAt }}</span>
                    </div>
                    <p class="comment-text">{{ r.content }}</p>
                  </div>
                </div>
              </div>

              <!-- 回复表单 -->
              <div v-if="replyTo === c.id" class="reply-form">
                <textarea v-model="replyContent" class="form-textarea" rows="2" placeholder="写下你的回复…" maxlength="200"></textarea>
                <div class="reply-actions">
                  <button class="btn btn-sm btn-ghost" @click="replyTo = null">取消</button>
                  <button class="btn btn-sm btn-primary" :disabled="commentLoading" @click="addReply(c.id)">发送</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-comments">暂无留言，来第一个提问吧</div>

        <!-- 发布留言 -->
        <div v-if="userStore.isLoggedIn()" class="comment-form">
          <textarea v-model="commentContent" class="form-textarea" rows="3" placeholder="对商品有任何疑问？在这里问卖家…" maxlength="200"></textarea>
          <div class="comment-form-footer">
            <span class="char-count">{{ commentContent.length }}/200</span>
            <button class="btn btn-primary btn-sm" :disabled="commentLoading || !commentContent.trim()" @click="addComment">发布留言</button>
          </div>
        </div>
        <div v-else class="login-hint">
          <router-link to="/login">登录</router-link> 后参与交流
        </div>
      </div>

      <!-- 评价区（状态：已售） -->
      <div v-if="item.status === 3" class="review-section card">
        <h3 class="section-heading">交易评价</h3>
        <div v-if="review" class="review-display">
          <div class="review-header">
            <span class="reviewer-name">{{ review.reviewerNickname }}</span>
            <el-rate :model-value="review.score" disabled show-score text-color="#f59e0b" />
          </div>
          <p class="review-content" v-if="review.content">{{ review.content }}</p>
          <span class="comment-time">{{ review.createdAt }}</span>
        </div>
        <div v-else-if="canReview" class="review-form">
          <p class="review-prompt">你已购买此商品，来评价这次交易吧</p>
          <div class="score-row">
            <span>评分：</span>
            <el-rate v-model="reviewScore" show-score />
          </div>
          <textarea v-model="reviewContent" class="form-textarea" rows="3" placeholder="分享你的购买体验…" maxlength="300"></textarea>
          <button class="btn btn-primary btn-sm" :disabled="reviewLoading" @click="submitReview" style="margin-top:10px">提交评价</button>
        </div>
        <div v-else class="no-comments">暂无评价</div>
      </div>
    </template>

    <div v-else class="empty-state">
      <div class="empty-icon">😕</div>
      <p>商品不存在或已被删除</p>
      <router-link to="/" class="btn btn-primary">返回首页</router-link>
    </div>

    <!-- 下单弹窗 -->
    <div v-if="showOrderModal" class="modal-overlay" @click.self="showOrderModal=false">
      <div class="modal card">
        <div class="modal-header">
          <h3>确认预购</h3>
          <button class="close-btn" @click="showOrderModal=false">✕</button>
        </div>
        <div class="modal-body">
          <div class="order-item-info">
            <strong>{{ item.title }}</strong>
            <span class="big-price">¥{{ item.price }}</span>
          </div>
          <div class="form-group">
            <label class="form-label">约定交易地点 <span class="req">*</span></label>
            <input v-model="orderForm.meetPlace" class="form-input" placeholder="如：图书馆门口、3号宿舍楼下" />
          </div>
          <div class="form-group">
            <label class="form-label">留言给卖家（选填）</label>
            <textarea v-model="orderForm.message" class="form-textarea" rows="3" placeholder="可以询问商品细节或备注…"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-ghost" @click="showOrderModal=false">取消</button>
          <button class="btn btn-primary" :disabled="orderLoading" @click="submitOrder">
            {{ orderLoading ? '提交中…' : '确认下单' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-page { padding: 20px 20px 60px; }

.breadcrumb { font-size: 13px; color: var(--text-muted); margin-bottom: 20px; }
.breadcrumb a { color: var(--primary); }
.breadcrumb .cur { color: var(--text); }

.detail-body {
  display: grid;
  grid-template-columns: 480px 1fr;
  gap: 32px;
  align-items: start;
}
@media (max-width: 900px) {
  .detail-body { grid-template-columns: 1fr; }
}

/* 图片 */
.main-img-wrap {
  position: relative;
  aspect-ratio: 4/3;
  border-radius: var(--radius);
  overflow: hidden;
  background: #f3f4f6;
}
.main-img { width: 100%; height: 100%; object-fit: contain; }
.main-img-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 80px; color: #d1d5db;
}
.status-badge-lg {
  position: absolute; top: 12px; right: 12px;
  font-size: 13px; padding: 4px 12px;
}
.thumb-list { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
.thumb {
  width: 70px; height: 70px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: border-color 0.2s;
}
.thumb.active { border-color: var(--primary); }

/* 信息 */
.item-title { font-size: 22px; font-weight: 700; line-height: 1.4; margin-bottom: 14px; }

.price-row { display: flex; align-items: baseline; gap: 10px; margin-bottom: 14px; }
.big-price { font-size: 28px; font-weight: 800; color: #dc2626; }
.ori-price { font-size: 14px; color: var(--text-muted); text-decoration: line-through; }
.discount {
  font-size: 12px; font-weight: 600;
  background: #fee2e2; color: #dc2626;
  padding: 2px 8px; border-radius: 4px;
}

.tag-row { display: flex; align-items: center; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
.stat-text { font-size: 13px; color: var(--text-muted); margin-left: auto; }

.seller-card {
  display: flex; align-items: center; gap: 12px;
  padding: 14px;
  background: var(--bg);
  border-radius: 10px;
  margin-bottom: 20px;
}
.seller-avatar {
  width: 44px; height: 44px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700;
  flex-shrink: 0;
}
.seller-detail { display: flex; flex-direction: column; gap: 2px; }
.seller-name { font-weight: 600; }
.seller-link { font-size: 13px; color: var(--primary); }

.section-label { font-size: 13px; font-weight: 600; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.desc-text { font-size: 14px; line-height: 1.8; color: var(--text); white-space: pre-wrap; }
.desc-section { margin-bottom: 16px; }

.meta-row { font-size: 13px; color: var(--text-muted); margin-bottom: 24px; }

.action-row { display: flex; gap: 12px; flex-wrap: wrap; }
.action-row .btn-lg { flex: 1; min-width: 120px; }

/* 弹窗 */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  z-index: 2000; display: flex; align-items: center; justify-content: center;
  padding: 20px;
}
.modal { width: 100%; max-width: 460px; }
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 20px;
  border-bottom: 1px solid var(--border);
}
.modal-header h3 { font-size: 17px; font-weight: 700; }
.close-btn { background: none; border: none; font-size: 18px; cursor: pointer; color: var(--text-muted); }
.modal-body { padding: 20px; }
.modal-footer {
  display: flex; gap: 10px; justify-content: flex-end;
  padding: 14px 20px;
  border-top: 1px solid var(--border);
}
.order-item-info {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
  font-size: 15px;
}
.req { color: var(--danger); }

/* 交流区 & 评价区 */
.comment-section, .review-section { margin-top: 32px; padding: 24px; }
.section-heading { font-size: 17px; font-weight: 700; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }

.comment-list { display: flex; flex-direction: column; gap: 16px; }
.comment-item { display: flex; gap: 12px; }
.comment-avatar {
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--primary); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px; flex-shrink: 0;
}
.comment-avatar.small { width: 28px; height: 28px; font-size: 12px; }
.comment-body { flex: 1; min-width: 0; }
.comment-head { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.comment-head strong { font-size: 13px; }
.comment-time { font-size: 12px; color: var(--text-muted); }
.comment-text { font-size: 14px; line-height: 1.6; margin: 0; color: var(--text); }
.reply-btn {
  font-size: 12px; color: var(--primary); background: none; border: none; cursor: pointer;
  padding: 0; margin-top: 4px;
}
.reply-btn:hover { text-decoration: underline; }

.reply-list { margin-top: 10px; padding-left: 16px; border-left: 2px solid var(--border); display: flex; flex-direction: column; gap: 10px; }
.reply-item { display: flex; gap: 10px; }

.reply-form { margin-top: 10px; }
.reply-form .form-textarea { width: 100%; padding: 8px 12px; font-size: 13px; border: 1px solid var(--border); border-radius: 8px; resize: vertical; }
.reply-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 6px; }

.comment-form { margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--border); }
.comment-form .form-textarea { width: 100%; padding: 10px 14px; font-size: 14px; border: 1px solid var(--border); border-radius: 8px; resize: vertical; }
.comment-form-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }
.char-count { font-size: 12px; color: var(--text-muted); }

.no-comments { text-align: center; padding: 32px 0; color: var(--text-muted); font-size: 14px; }
.login-hint { text-align: center; padding: 16px 0; color: var(--text-muted); font-size: 14px; }
.login-hint a { color: var(--primary); }

.review-display { padding: 4px 0; }
.review-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.reviewer-name { font-weight: 600; font-size: 14px; }
.review-content { font-size: 14px; line-height: 1.6; color: var(--text); margin-bottom: 8px; }
.review-prompt { font-size: 14px; color: var(--text-muted); margin-bottom: 12px; }
.score-row { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 14px; }
.review-form .form-textarea { width: 100%; padding: 10px 14px; font-size: 14px; border: 1px solid var(--border); border-radius: 8px; resize: vertical; }

/* 锁定订单买家信息卡 */
.lock-info-card {
  margin-top: 16px; padding: 16px;
  background: #f9fafb; border: 1px solid var(--border); border-radius: 10px;
}
.lock-info-title { font-size: 14px; font-weight: 700; margin-bottom: 12px; color: var(--text); }
.lock-info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.lock-info-item { display: flex; flex-direction: column; gap: 2px; }
.lock-info-label { font-size: 12px; color: var(--text-muted); }
.lock-info-value { font-size: 14px; color: var(--text); font-weight: 500; }
.lock-info-msg { margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--border); }
.lock-info-msg p { margin: 4px 0 0; font-size: 14px; color: var(--text); line-height: 1.5; }

.lock-status-text { font-size: 16px; color: var(--text-muted); font-weight: 500; padding: 10px 0; }
.sold-text { font-size: 16px; color: var(--text-muted); font-weight: 500; }

.btn-success { background: #16a34a; color: #fff; border: none; border-radius: 8px; padding: 10px 24px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.15s; }
.btn-success:hover { background: #15803d; }
.btn-success:disabled { background: #86efac; cursor: not-allowed; }
</style>
