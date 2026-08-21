import axios from 'axios'
import { useUserStore } from '../stores/user'
import router from '../router'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
  withCredentials: true
})

request.interceptors.response.use(
  res => {
    const data = res.data
    if (data.code === 401) {
      const userStore = useUserStore()
      userStore.logout()
      router.push('/login')
      return Promise.reject(new Error('请先登录'))
    }
    if (data.code !== 200) {
      return Promise.reject(new Error(data.message || '操作失败'))
    }
    return data
  },
  err => {
    const msg = err.response?.data?.message || err.message || '网络错误'
    return Promise.reject(new Error(msg))
  }
)

export default request
