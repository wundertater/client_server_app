<template>
  <div class="app-container">
    <!-- Левая панель -->
    <SidePanel
      :section="currentSection"
      @selectSection="currentSection = $event"
      @apply-filters="onApplyFilters"
    />

    <!-- Правая область -->
    <div class="content-area">
      <component :is="currentComponent" :filters="appliedFilters" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import SidePanel from "./components/SidePanel.vue";
import InstructorsTable from "./components/InstructorsTable.vue";
import StudentsTable from "./components/StudentsTable.vue";

const currentSection = ref("instructors");
const appliedFilters = ref({});

const currentComponent = computed(() =>
  currentSection.value === "instructors" ? InstructorsTable : StudentsTable
);

function onApplyFilters(filters) {
  appliedFilters.value = { ...filters };
}
</script>

<style scoped>
.app-container {
  display: flex; /* ВАЖНО: горизонтальное расположение */
  height: 100vh;
  background: linear-gradient(to bottom right, #e3f2fd, #bbdefb);
}

/* Левая панель фиксированной ширины */
.app-container > *:first-child {
  flex-shrink: 0;
}

/* Правая часть занимает всё оставшееся место */
.content-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
