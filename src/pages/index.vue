<script setup lang="ts">
import type { MyRecord } from '~/types'
import { useTimeAgo, useTimeoutFn } from '@vueuse/core'
import {supabase} from '~/supabase'


const latestPhoneRecord = ref({} as MyRecord)

async function fetchData () {
  const latestPhoneResponse = await supabase
            .from("records")
            .select()
            .eq("source", 1) // from phone
            .order("updated_at", { ascending: false })
            .limit(1)
  latestPhoneRecord.value = latestPhoneResponse?.data?.[0] ?? {}
}

const timeAgo = computed(() => useTimeAgo(latestPhoneRecord.value?.updated_at))
const batteryIcon = computed(() =>
         `i-material-symbols:battery-${(Math.floor(latestPhoneRecord.value?.battery / 16 || 0))}-bar`
)
const batteryColor = computed(() => {
  const battery = latestPhoneRecord.value?.battery
  if (!battery) {
    return 'text-gray'
  } else if (battery < 20) {
    return 'text-red'
  } else if (battery < 50) {
    return 'text-yellow'
  } else {
    return 'text-green'
  }
})

useTimeoutFn(async () => {
  await fetchData()
}, 300, { immediate: true })

onMounted(async () => {
  await fetchData()
})


</script>

<template>
  <div>
    <h1 class="font-bold text-5xl gradient-title inline-block">我在干嘛?</h1>
    <div flex gap-1 text-3xl mt-8 justify-center>
      <div font-bold dark:text-white:30 text-gray:90>手机</div>
      <i :class="[batteryIcon, batteryColor]" mr-5></i>
      <div font-bold>{{ latestPhoneRecord?.app || "Loading" }}</div>
    </div>
    <div flex gap-5 text-3xl my-4 justify-center>
      <div font-bold dark:text-white:30 text-gray:90>电脑</div>
      <div font-bold>TODO</div>
    </div>
    <div flex gap-3 text-xl my-4 justify-center text-white font-bold>
      <span dark:text-white:30 text-gray:90>上次更新</span>
      <span>{{ timeAgo || "Loading" }}</span>
    </div>

  </div>
</template>


<style scoped>


.gradient-title {
  background: linear-gradient(to right, #0d5661, #33a6b8);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}

.dark .gradient-title {
  background: linear-gradient(to right, #d9ab42, #fad689);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}
</style>
