<script lang="ts">
import { Icon } from '@arco-design/web-vue'

const IconHomeFill = Icon.addFromIconFontCn({
  src: '//at.alicdn.com/t/c/font_5104981_ao1ihfgyt7.js',
})
export default {
  components: {
    IconHomeFill,
  },
}
</script>

<template>
  <icon-home-fill type="icon-home-fill" :size="18" />
</template>
