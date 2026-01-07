<script lang="ts">
import { Icon } from '@arco-design/web-vue'

const IconCommonFill = Icon.addFromIconFontCn({
  src: '//at.alicdn.com/t/c/font_5105080_pzeu8r34y7m.js',
})
export default {
  components: {
    IconCommonFill,
  },
}
</script>

<template>
  <icon-common-fill type="icon-common-fill" :size="18" />
</template>
