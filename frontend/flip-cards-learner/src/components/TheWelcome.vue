<script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import SupportIcon from './icons/IconSupport.vue'
</script>

<template>
  <WelcomeItem>
    <template #icon>
      <DocumentationIcon />
    </template>
    <template #heading>Documentation</template>

    Flip Card Learning App
    <a href="https://github.com/hristiyandudev55/python-flipcards-learner/blob/main/README.md" target="_blank" rel="noopener">official documentation</a>
    provides you with all information you need to get started.
  </WelcomeItem>


  <WelcomeItem>
    <template #icon>
      <SupportIcon />
    </template>
    <template #heading>Feedback</template>

    Your feedback is essential for my growth. Help me improve by sharing your thoughts and suggestions on my official GitHub profile
    <a href="https://github.com/hristiyandudev55" target="_blank" rel="noopener">hristiyandudev55</a>.
  </WelcomeItem>

</template>
