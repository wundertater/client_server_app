<template>
  <div class="w-72 bg-blue-200 flex flex-col p-2">
    <!-- Переключатели -->
    <div class="flex mb-2">
      <button
        :class="[
          'flex-1 p-2 rounded-l',
          section === 'instructors' ? 'bg-blue-500 text-white' : 'bg-white',
        ]"
        @click="$emit('selectSection', 'instructors')"
      >
        Преподаватели
      </button>
      <button
        :class="[
          'flex-1 p-2 rounded-r',
          section === 'students' ? 'bg-blue-500 text-white' : 'bg-white',
        ]"
        @click="$emit('selectSection', 'students')"
      >
        Студенты
      </button>
    </div>

    <!-- Панель фильтров -->
    <FilterPanel @apply-filters="$emit('apply-filters', $event)" />
  </div>
</template>

<script setup>
import FilterPanel from "./FilterPanel.vue";

const props = defineProps({
  section: String,
});
</script>

<style scoped>
button {
  transition: background 0.2s;
}
</style>
