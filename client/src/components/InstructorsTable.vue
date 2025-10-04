<template>
  <div class="instructors-table">

    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="instructors.length === 0" class="no-data">
      Нет данных
    </div>

    <div v-else class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Имя Фамилия</th>
            <th>Кафедра</th>
            <th>Группы</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inst in instructors" :key="inst.id">
            <td>{{ inst.first_name }} {{ inst.last_name }}</td>
            <td>{{ inst.department?.name || "-" }}</td>
            <td>{{ inst.groups.join(", ") }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { getInstructors } from "@/api";

const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
});

const instructors = ref([]);
const loading = ref(false);

// Загружает преподавателей с заданными параметрами
const loadInstructors = async (filters = {}) => {
  loading.value = true;
  try {
    // Формируем query параметры
    const params = {};

    if (filters.departments?.length) params.d = filters.departments;
    if (filters.groups?.length) params.g = filters.groups;
    if (filters.firstName) params.fn = filters.firstName;
    if (filters.lastName) params.ln = filters.lastName;

    const { data } = await getInstructors(params);
    instructors.value = data;
  } catch (err) {
    console.error("Ошибка загрузки преподавателей:", err);
  } finally {
    loading.value = false;
  }
};

// При первом запуске загружаем всех
onMounted(() => loadInstructors());

// Следим за изменением фильтров (когда нажимают "Применить")
watch(
  () => props.filters,
  (newFilters) => {
    loadInstructors(newFilters);
  },
  { deep: true }
);
</script>

<style scoped>
.instructors-table {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

h3 {
  margin-bottom: 10px;
  font-size: 18px;
  color: #0d47a1;
}

.table-wrapper {
  overflow-y: auto;
  max-height: 80vh;
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-family: sans-serif;
}

th {
  background: #e3f2fd;
  text-align: left;
  padding: 8px;
  border-bottom: 1px solid #ccc;
}

td {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.loading,
.no-data {
  text-align: center;
  padding: 20px;
  color: #555;
}
</style>
