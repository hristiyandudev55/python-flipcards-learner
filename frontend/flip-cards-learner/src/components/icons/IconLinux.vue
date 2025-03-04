<script setup>
import { getAssetUrl } from '@/services/assetService';
</script>

<template>
  <img :src="getAssetUrl('Linux.png')" alt="Linux Icon" width="32" height="32" />
</template>