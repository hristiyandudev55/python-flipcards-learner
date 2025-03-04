<script setup>
import { getAssetUrl } from '@/services/assetService';
</script>

<template>
  <img :src="getAssetUrl('githubactions.png')" alt="Github Actions Icon" width="32" height="32" />
</template>