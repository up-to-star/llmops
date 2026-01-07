<script lang="ts">
import { Icon } from '@arco-design/web-vue'

const IconUserFill = Icon.addFromIconFontCn({
  src: '//at.alicdn.com/t/c/font_5105054_3ujnfxm5xfu.js',
})
export default {
  components: {
    IconUserFill,
  },
}
</script>

<template>
  <icon-user-fill type="icon-user-fill" :size="18" />
</template>
