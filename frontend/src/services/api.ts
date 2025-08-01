import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

// 剧本解析
export const parseScript = async (scriptText: string) => {
  const response = await api.post('/scripts/parse', {
    script_text: scriptText,
  })
  return response.data
}

// 角色生成
export const generateCharacter = async (description: string) => {
  const response = await api.post('/characters/generate', {
    description,
  })
  return response.data
}

// 使用图片生成角色
export const generateCharacterWithImage = async (description: string, imageFile: File) => {
  const formData = new FormData()
  formData.append('description', description)
  formData.append('image', imageFile)
  
  const response = await api.post('/characters/generate-with-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// 场景生成
export const generateScene = async (description: string) => {
  const response = await api.post('/scenes/generate', {
    description,
  })
  return response.data
}

// 视频生成
export const generateVideo = async (scriptData: any) => {
  const response = await api.post('/videos/generate', scriptData)
  return response.data
}

// 获取生成状态
export const getGenerationStatus = async (taskId: string) => {
  const response = await api.get(`/status/${taskId}`)
  return response.data
}

export default api