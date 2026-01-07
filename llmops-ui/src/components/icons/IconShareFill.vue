<script lang="ts">
import { Icon } from '@arco-design/web-vue'

const IconShareFill = Icon.addFromIconFontCn({
  src: '//at.alicdn.com/t/c/font_5105084_882acswxnzb.js',
})
export default {
  components: {
    IconShareFill,
  },
}
</script>

<template>
  <icon-share-fill type="icon-share-fill" :size="18" />
</template>
