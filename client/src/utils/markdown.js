// src/utils/markdown.js
import MarkdownIt from 'markdown-it';
import { katex } from '@mdit/plugin-katex';
import DOMPurify from 'dompurify';
// 千万别删这行，否则公式会变成乱码字体
import 'katex/dist/katex.min.css';

// 1. 初始化 markdown-it
const md = new MarkdownIt({
    html: true,      // 允许 HTML 标签
    linkify: true,   // 自动把网址转成链接
    breaks: true,    // 允许直接回车换行（聊天场景必备！）
});

// 2. 挂载 KaTeX 插件
md.use(katex, {
    throwOnError: false, // AI 生成了一半的公式语法错误时，不阻断整个渲染
    delimiters: 'all',
});

// 3. 导出渲染函数
export function renderMarkdown(text) {
    if (!text) return '';
    const rawHtml = md.render(text);
    // 清洗 HTML，防止 XSS 注入
    return DOMPurify.sanitize(rawHtml);
}