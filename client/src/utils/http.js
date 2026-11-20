// 统一的网络错误信息处理，避免把 "Failed to fetch" 之类的原始报错直接展示给用户

export async function readError(response, prefix) {
  let detail = `服务异常（HTTP ${response.status}）`

  if (response.status === 401) {
    detail = '登录状态已失效，请重新登录'
  } else {
    try {
      const data = await response.json()
      const raw = data && data.detail
      if (typeof raw === 'string' && raw.trim()) {
        detail = raw
      } else if (Array.isArray(raw) && raw.length) {
        detail = raw.map((item) => item.msg || JSON.stringify(item)).join('；')
      } else if (raw) {
        detail = JSON.stringify(raw)
      }
    } catch {
      // 响应不是 JSON，保留状态码信息
    }
  }

  return prefix ? `${prefix}：${detail}` : detail
}

export function toErrorMessage(error, fallback = '操作失败，请稍后重试') {
  if (!error) return fallback
  const message = typeof error === 'string' ? error : error.message
  if (!message) return fallback
  if (error instanceof TypeError && /fetch|network/i.test(message)) {
    return '无法连接服务器，请检查网络后重试'
  }
  return message
}
