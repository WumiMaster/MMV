import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

// 检查证书文件是否存在
const certPath = path.resolve(__dirname, '../cert.pem')
const keyPath = path.resolve(__dirname, '../key.pem')
const useHttps = fs.existsSync(certPath) && fs.existsSync(keyPath)

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5174,
    host: '0.0.0.0',
    https: useHttps ? {
      cert: fs.readFileSync(certPath),
      key: fs.readFileSync(keyPath)
    } : false,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        secure: false
      }
    }
  }
})
