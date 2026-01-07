<script lang="ts">
import { Icon } from '@arco-design/web-vue'

const IconRobotFill = Icon.addFromIconFontCn({
  src: '//at.alicdn.com/t/c/font_5105079_mb1nyxzu95f.js',
})
export default {
  components: {
    IconRobotFill,
  },
}
</script>

<template>
  <icon-robot-fill type="icon-robot-fill" :size="18" />
</template>
