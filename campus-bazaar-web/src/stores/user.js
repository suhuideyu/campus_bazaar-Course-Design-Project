import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userApi } from '../api/index'

export const useUserStore = defineStore('user', () => {
  const user = ref(JSON.parse(localStorage.getItem('cbUser') || 'null'))

  function setUser(u) {
    user.value = u
    if (u) {
      localStorage.setItem('cbUser', JSON.stringify(u))
    } else {
      localStorage.removeItem('cbUser')
    }
  }

  async function fetchMe() {
    try {
      const res = await userApi.getMe()
      setUser(res.data)
    } catch {
      setUser(null)
    }
  }

  function logout() {
    setUser(null)
  }

  const isLoggedIn = () => !!user.value

  return { user, setUser, fetchMe, logout, isLoggedIn }
})
