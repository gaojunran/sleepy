<script setup lang="ts">
import type { MyRecord } from '~/types'
import { useTimeAgo, useTimeoutFn } from '@vueuse/core'
import { supabase } from '~/supabase'

const latestPhoneRecord = ref({} as MyRecord)
const latestPcRecord = ref({} as MyRecord)

async function fetchData() {
  const fetchPhone = async () => await supabase
    .from('records')
    .select()
    .eq('source', 1) // from phone
    .order('updated_at', { ascending: false })
    .limit(1)
  const fetchPc = async () => await supabase
    .from('records')
    .select()
    .eq('source', 2) // from pc
    .order('updated_at', { ascending: false })
    .limit(1)
  const [latestPhoneResponse, latestPcResponse] = await Promise.all([fetchPhone(), fetchPc()])
  latestPhoneRecord.value = latestPhoneResponse?.data?.[0] ?? {}
  latestPcRecord.value = latestPcResponse?.data?.[0] ?? {}
}

const timeAgo = computed(() => useTimeAgo(latestPhoneRecord.value?.updated_at))
const batteryIcon = computed(() =>
  `i-material-symbols:battery-${(Math.floor(latestPhoneRecord.value?.battery / 16 || 0))}-bar`,
)
const batteryColor = computed(() => {
  const battery = latestPhoneRecord.value?.battery
  if (!battery) {
    return 'text-gray'
  }
  else if (battery < 20) {
    return 'text-red'
  }
  else if (battery < 60) {
    return 'text-yellow'
  }
  else {
    return 'text-green-700'
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
    <h1 class="gradient-title text-5xl font-bold inline-block">
      我在干嘛?
    </h1>
    <div text-3xl mt-8 flex items-end justify-center>
      <div text-gray:90 font-bold mr-1 dark:text-white:30>
        手机
      </div>
      <i :class="[batteryIcon, batteryColor]" />
      <div :class="[batteryColor]" text-lg font-bold mr-4>
        {{ latestPhoneRecord?.battery || "" }}%
      </div>
      <div font-bold>
        {{ latestPhoneRecord?.app || "Loading" }}
      </div>
    </div>
    <div text-3xl my-4 flex justify-center>
      <div text-gray:90 font-bold mr-4 dark:text-white:30>
        电脑
      </div>
      <div font-bold>
        {{ latestPcRecord?.app || "Loading" }}
      </div>
    </div>
    <div text-xl text-white font-bold my-4 flex gap-3 justify-center>
      <span text-gray:90 dark:text-white:30>上次更新</span>
      <span text-black dark:text-white>{{ timeAgo || "Loading" }}</span>
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
