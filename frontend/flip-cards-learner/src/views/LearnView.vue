<script setup>
import { useRouter } from 'vue-router'
import WelcomeItem from '../components/WelcomeItem.vue'
import DocumentationIcon from '../components/icons/IconDocumentation.vue'
import IconOOP from '../components/icons/IconOOP.vue'
import IconDocker from '../components/icons/IconDocker.vue'
import IconGitHubAction from '../components/icons/IconGitHubAction.vue'
import IconLinux from '../components/icons/IconLinux.vue'
import IconHTML from '../components/icons/IconHTML.vue'
import IconDSA from '../components/icons/IconDSA.vue'
import IconAzure from '../components/icons/IconAzure.vue'

const router = useRouter()

const navigateToCategory = (category) => {
  router.push(`/category/${category.toLowerCase()}`)
}
</script>

<template>
  <div class="main-content">
    <div class="info-card full-width">
      <WelcomeItem @click="navigateToCategory('OOP')">
        <template #icon>
          <IconOOP />
        </template>
        <template #heading>Object-Oriented Programming (OOP)</template>
        Master object-oriented programming concepts in Python including classes, inheritance, and polymorphism
      </WelcomeItem>

      <WelcomeItem @click="navigateToCategory('DSA')">
        <template #icon>
          <IconDSA />
        </template>
        <template #heading>Data Structures & Algorithms (DSA)</template>
        Learn essential data structures and algorithmic concepts in Python
      </WelcomeItem>

      <WelcomeItem @click="navigateToCategory('WEB')">
        <template #icon>
          <IconHTML />
        </template>
        <template #heading>Web Development (WEB)</template>
        Explore web development using Python frameworks like FastAPI
      </WelcomeItem>

      <WelcomeItem @click="navigateToCategory('DOCKER')">
        <template #icon>
          <IconDocker />
        </template>
        <template #heading>Docker Containerization</template>
        Learn Docker fundamentals, container management, and deployment strategies
      </WelcomeItem>

      <WelcomeItem @click="navigateToCategory('CI_CD')">
        <template #icon>
          <IconGitHubAction />
        </template>
        <template #heading>CI/CD Workflow</template>
        Master continuous integration and deployment practices using modern tools
      </WelcomeItem>

      <WelcomeItem @click="navigateToCategory('AZURE')">
        <template #icon>
          <IconAzure />
        </template>
        <template #heading>Azure Cloud Services</template>
        Explore Microsoft Azure cloud services, deployment, and cloud architecture
      </WelcomeItem>

      <WelcomeItem @click="navigateToCategory('LINUX')">
        <template #icon>
          <IconLinux />
        </template>
        <template #heading>Linux Administration</template>
        Learn essential Linux commands, system administration, and shell scripting
      </WelcomeItem>
    </div>
  </div>
</template>

<style scoped>
.main-content {
  padding: 20px;
}

.info-card {
  background: var(--color-background);
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
}

.info-card :deep(.item) {
  transition: transform 0.2s;
}

.info-card :deep(.item:hover) {
  transform: translateX(10px);
  background-color: var(--color-background-soft);
  border-radius: 8px;
}
</style>
