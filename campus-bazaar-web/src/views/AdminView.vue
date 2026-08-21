<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '../api/index'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeTab = ref('users')

// ========== 用户管理 ==========
const users = ref([])
const userTotal = ref(0)
const userPage = ref(1)
const userPageSize = ref(10)
const userLoading = ref(false)

async function loadUsers() {
  userLoading.value = true
  try {
    const res = await adminApi.listUsers(userPage.value, userPageSize.value)
    users.value = res.data.list
    userTotal.value = res.data.total
  } catch { }
  userLoading.value = false
}

async function toggleUserStatus(user) {
  const newStatus = user.status === 1 ? 0 : 1
  const action = newStatus === 0 ? '禁用' : '启用'
  try {
    await ElMessageBox.confirm(`确定要${action}用户「${user.nickname}」吗？`, '提示', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    })
    await adminApi.updateUserStatus(user.id, newStatus)
    user.status = newStatus
    ElMessage.success(`已${action}用户`)
  } catch { }
}

function onUserPageChange(page) {
  userPage.value = page
  loadUsers()
}

// ========== 商品管理 ==========
const items = ref([])
const itemTotal = ref(0)
const itemPage = ref(1)
const itemPageSize = ref(10)
const itemStatus = ref(null)
const itemKeyword = ref('')
const itemLoading = ref(false)

const statusOptions = [
  { label: '全部状态', value: null },
  { label: '待审核', value: 0 },
  { label: '在售', value: 1 },
  { label: '锁定', value: 2 },
  { label: '已售', value: 3 },
  { label: '下架', value: 4 }
]

const statusMap = { 0: '待审核', 1: '在售', 2: '锁定', 3: '已售', 4: '下架' }
const statusColorMap = { 0: '#e6a23c', 1: '#67c23a', 2: '#f56c6c', 3: '#909399', 4: '#909399' }

async function loadItems() {
  itemLoading.value = true
  try {
    const res = await adminApi.listItems(itemPage.value, itemPageSize.value, itemStatus.value, itemKeyword.value)
    items.value = res.data.list
    itemTotal.value = res.data.total
  } catch { }
  itemLoading.value = false
}

async function updateItemStatus(item, newStatus) {
  try {
    await adminApi.updateItemStatus(item.id, newStatus)
    item.status = newStatus
    ElMessage.success('商品状态已更新')
  } catch { }
}

function onItemPageChange(page) {
  itemPage.value = page
  loadItems()
}

function searchItems() {
  itemPage.value = 1
  loadItems()
}

onMounted(() => {
  loadUsers()
  loadItems()
})
</script>

<template>
  <div class="admin-container">
    <h1 class="admin-title">管理员面板</h1>

    <el-tabs v-model="activeTab" class="admin-tabs">
      <!-- 用户管理 Tab -->
      <el-tab-pane label="用户管理" name="users">
        <el-table :data="users" v-loading="userLoading" stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="username" label="用户名" width="120" />
          <el-table-column prop="nickname" label="昵称" width="140" />
          <el-table-column prop="phone" label="手机号" width="130" />
          <el-table-column prop="school" label="学校" width="120" />
          <el-table-column prop="creditScore" label="信用分" width="80" />
          <el-table-column label="角色" width="80">
            <template #default="{ row }">
              <el-tag :type="row.role === 1 ? 'danger' : 'info'" size="small">
                {{ row.role === 1 ? '管理员' : '用户' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.status === 1 ? 'success' : 'danger'" size="small">
                {{ row.status === 1 ? '正常' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createdAt" label="注册时间" width="170" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <el-button
                v-if="row.role !== 1"
                :type="row.status === 1 ? 'danger' : 'success'"
                size="small"
                @click="toggleUserStatus(row)"
              >
                {{ row.status === 1 ? '禁用' : '启用' }}
              </el-button>
              <span v-else style="color:#909399;font-size:12px">不可操作</span>
            </template>
          </el-table-column>
        </el-table>
        <div style="display:flex;justify-content:center;margin-top:20px">
          <el-pagination
            background
            layout="prev, pager, next, total"
            :total="userTotal"
            :page-size="userPageSize"
            v-model:current-page="userPage"
            @current-change="onUserPageChange"
          />
        </div>
      </el-tab-pane>

      <!-- 商品管理 Tab -->
      <el-tab-pane label="商品管理" name="items">
        <div class="item-filters">
          <el-select v-model="itemStatus" placeholder="状态筛选" clearable style="width:140px" @change="searchItems">
            <el-option v-for="o in statusOptions" :key="o.value" :label="o.label" :value="o.value" />
          </el-select>
          <el-input
            v-model="itemKeyword"
            placeholder="搜索商品标题"
            clearable
            style="width:240px"
            @keyup.enter="searchItems"
            @clear="searchItems"
          >
            <template #append>
              <el-button @click="searchItems">搜索</el-button>
            </template>
          </el-input>
        </div>

        <el-table :data="items" v-loading="itemLoading" stripe style="width:100%;margin-top:12px">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="标题" min-width="160">
            <template #default="{ row }">
              <router-link :to="'/item/' + row.id" class="item-link">{{ row.title }}</router-link>
            </template>
          </el-table-column>
          <el-table-column prop="sellerNickname" label="卖家" width="120">
            <template #default="{ row }">
              <router-link :to="'/seller/' + row.sellerId" class="seller-link">{{ row.sellerNickname }}</router-link>
            </template>
          </el-table-column>
          <el-table-column prop="categoryName" label="分类" width="100" />
          <el-table-column prop="price" label="价格" width="90">
            <template #default="{ row }">
              <span style="color:#f56c6c;font-weight:600">¥{{ row.price }}</span>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="90">
            <template #default="{ row }">
              <el-tag :color="statusColorMap[row.status]" effect="dark" size="small">
                {{ statusMap[row.status] || row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="viewCount" label="浏览" width="70" />
          <el-table-column prop="favCount" label="收藏" width="70" />
          <el-table-column prop="createdAt" label="发布时间" width="170" />
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-select
                :model-value="row.status"
                size="small"
                style="width:110px"
                @change="(val) => updateItemStatus(row, val)"
              >
                <el-option v-for="o in statusOptions.slice(1)" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </template>
          </el-table-column>
        </el-table>
        <div style="display:flex;justify-content:center;margin-top:20px">
          <el-pagination
            background
            layout="prev, pager, next, total"
            :total="itemTotal"
            :page-size="itemPageSize"
            v-model:current-page="itemPage"
            @current-change="onItemPageChange"
          />
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.admin-container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }
.admin-title { font-size: 24px; font-weight: 700; color: var(--text); margin-bottom: 20px; }
.admin-tabs { --el-tabs-header-height: 44px; }
.item-filters { display: flex; gap: 12px; align-items: center; }
.seller-link { color: var(--primary); text-decoration: none; font-weight: 500; }
.seller-link:hover { text-decoration: underline; }
.item-link { color: var(--primary); text-decoration: none; }
.item-link:hover { text-decoration: underline; }
</style>
