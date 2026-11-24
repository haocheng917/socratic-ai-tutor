import { fetchEventSource } from '@microsoft/fetch-event-source'
import { readError } from './http.js'

const DONE = '[DONE]'

// 调 /tutor/chat 并消费后端 SSE 事件：
//   data: {"type":"content","content":"..."}
//   data: {"type":"title","title":"..."}
//   data: [DONE]
export async function streamChat({
  baseUrl,
  token,
  conversationId,
  content,
  onContent,
  onTitle,
  signal,
}) {
  let receivedDone = false

  await fetchEventSource(`${baseUrl}/tutor/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ conversation_id: conversationId, content }),
    signal,
    // 这个库默认在页面隐藏时断开、切回来再重连；聊天请求不能这样
    openWhenHidden: true,

    async onopen(response) {
      if (!response.ok) {
        // 401 登录失效、404 会话不存在等，在这里就能拿到状态码和 detail
        throw new Error(await readError(response, '发送失败'))
      }
      const contentType = response.headers.get('content-type') || ''
      if (!contentType.includes('text/event-stream')) {
        throw new Error('服务端返回的不是流式响应')
      }
    },

    onmessage(message) {
      if (message.data === DONE) {
        receivedDone = true
        return
      }

      let event
      try {
        event = JSON.parse(message.data)
      } catch {
        // 单个脏事件不打断整个回复
        console.warn('无法解析的 SSE 事件，已跳过：', message.data)
        return
      }

      if (event.type === 'content' && typeof event.content === 'string') {
        onContent(event.content)
      } else if (event.type === 'title' && event.title) {
        onTitle(event.title)
      } else if (event.type === 'error') {
        // 后端以后如果用事件传业务错误，这里能接住
        throw new Error(event.message || '服务端处理失败')
      }
    },

    onclose() {
      // 连接正常关闭，但没收到 [DONE]：说明流被截断了
      if (!receivedDone) {
        throw new Error('回复没有正常结束，请重试')
      }
    },

    // 关键：这个库默认失败后每 1 秒自动重连。
    // /chat 每次调用都会把用户消息写进数据库，重连会造成重复消息，
    // 所以必须抛错来阻止它自动重试。
    onerror(error) {
      throw error
    },
  })
}
