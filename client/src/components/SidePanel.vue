<template>
  <div class="w-72 bg-blue-200 flex flex-col p-3 rounded-r-lg shadow-md">
    <!-- Переключатели -->
    <div class="flex mb-3 bg-white rounded-lg overflow-hidden shadow-sm">
      <button
        :class="[
          'flex-1 py-2 font-semibold transition-all duration-200',
          section === 'instructors'
            ? 'bg-blue-600 text-white shadow-md scale-[1.02]'
            : 'bg-white text-gray-700 hover:bg-blue-100',
        ]"
        @click="$emit('selectSection', 'instructors')"
      >
        Преподаватели
      </button>

      <button
        :class="[
          'flex-1 py-2 font-semibold transition-all duration-200',
          section === 'students'
            ? 'bg-blue-600 text-white shadow-md scale-[1.02]'
            : 'bg-white text-gray-700 hover:bg-blue-100',
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
  transition: all 0.25s ease;
}

button:hover {
  filter: brightness(1.05);
}

/* Активное состояние можно усилить доп. рамкой */
button.active {
  border-bottom: 3px solid #1e40af; /* насыщенно-синий */
}
</style>
