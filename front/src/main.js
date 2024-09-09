import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-light.css'
import App from './App.vue'

const app = createApp(App)
app.directive('highlight', function (el) {
  const blocks = el.querySelectorAll('pre code');
  blocks.forEach((block) => {
    hljs.highlightBlock(block);
  });
});
app.use(hljs.vuePlugin) 
app.use(ElementPlus)
app.mount('#app')

