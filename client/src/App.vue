<template>
  <div class="app">
    <div class="content">
      <FilterPanel @apply-filters="onApplyFilters" />
      <InstructorsTable :filters="appliedFilters" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import FilterPanel from "./components/FilterPanel.vue";
import InstructorsTable from "./components/InstructorsTable.vue";

const appliedFilters = ref({});

const onApplyFilters = (filters) => {
  appliedFilters.value = { ...filters };
};
</script>

<style scoped>
.app {
  background: linear-gradient(to bottom right, #e3f2fd, #bbdefb);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.content {
  display: flex;
  gap: 20px;
  width: 80%;
}
</style>
