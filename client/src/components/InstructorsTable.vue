<template>
  <div class="instructors-table">
    <div class="header-row">
      <h3>Преподаватели</h3>

      <!-- Кнопки действий -->
      <div class="action-buttons">
        <button class="hire-btn" @click="showAddModal = true">Нанять</button>
        <button class="fire-btn" @click="fireSelected">Уволить</button>
      </div>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="instructors.length === 0" class="no-data">Нет данных</div>

    <div v-else class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th class="checkbox-col">
              <input
                type="checkbox"
                :checked="allSelected"
                @change="toggleSelectAll"
              />
            </th>
            <th>Имя Фамилия</th>
            <th>Кафедра</th>
            <th>Группы</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inst in instructors" :key="inst.id">
            <td class="checkbox-col">
              <input type="checkbox" v-model="selectedIds" :value="inst.id" />
            </td>
            <td class="clickable" @click="openInstructor(inst.id)">
              {{ inst.first_name }} {{ inst.last_name }}
            </td>
            <td>{{ inst.department?.name || "-" }}</td>
            <td>{{ inst.groups.join(", ") }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модалка просмотра/редактирования преподавателя -->
    <InstructorViewEdit
      v-if="showModal"
      :instructorId="selectedId"
      @close="closeModal"
      @updated="handleInstructorUpdated"
    />

    <!-- ✅ Модалка добавления преподавателя -->
    <AddPersonModal
  v-if="showAddModal"
  :visible="showAddModal"
  type="instructor"
  @close="showAddModal = false"
  @save="handleInstructorAdded"
/>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { onBalanceDone } from "@/websocket";
import { getInstructors, deleteInstructor, addInstructor } from "@/api";
import InstructorViewEdit from "./InstructorViewEdit.vue";
import AddPersonModal from "./AddPersonModal.vue";

const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
});

const instructors = ref([]);
const loading = ref(false);
const showModal = ref(false);
const selectedId = ref(null);
const selectedIds = ref([]);
const showAddModal = ref(false);

let unsubscribe = null;

// 📥 Загрузка преподавателей
const loadInstructors = async (filters = {}) => {
  loading.value = true;
  try {
    const params = {};
    if (filters.departments?.length) params.d = filters.departments;
    if (filters.groups?.length) params.g = filters.groups;
    if (filters.firstName) params.fn = filters.firstName;
    if (filters.lastName) params.ln = filters.lastName;

    const { data } = await getInstructors(params);
    instructors.value = data;
    selectedIds.value = [];
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleInstructorAdded = async () => {
  alert("Преподаватель успешно добавлен!");
  showAddModal.value = false;
};


// 🧍‍♂️ Просмотр/редактирование
const openInstructor = (id) => {
  selectedId.value = id;
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
  selectedId.value = null;
};
const handleInstructorUpdated = async () => {
  await loadInstructors(props.filters);
};

// ✅ Добавление нового преподавателя
const handleAddInstructor = async (formData) => {
  try {
    await addInstructor(formData);
    alert("Преподаватель успешно добавлен!");
    showAddModal.value = false;
    await loadInstructors(props.filters);
  } catch (err) {
    console.error(err);
    alert("Ошибка при добавлении преподавателя.");
  }
};

// 🔘 Выделение чекбоксов
const allSelected = computed(
  () =>
    instructors.value.length > 0 &&
    selectedIds.value.length === instructors.value.length
);

const toggleSelectAll = () => {
  if (allSelected.value) selectedIds.value = [];
  else selectedIds.value = instructors.value.map((i) => i.id);
};

// 🔥 Увольнение выбранных
const fireSelected = async () => {
  if (selectedIds.value.length === 0) {
    alert("Выберите хотя бы одного преподавателя для увольнения.");
    return;
  }

  if (!confirm("Вы действительно хотите уволить выбранных преподавателей?")) {
    return;
  }

  const failed = [];
  for (const id of selectedIds.value) {
    const instructor = instructors.value.find((i) => i.id === id);
    try {
      await deleteInstructor(id);
    } catch (err) {
      failed.push(
        `${instructor?.first_name || ""} ${instructor?.last_name || ""}`.trim()
      );
    }
  }

  if (failed.length > 0) {
    alert(`Не удалось уволить: ${failed.join(", ")}`);
  } else {
    alert("Все выбранные преподаватели успешно уволены!");
  }

  await loadInstructors(props.filters);
};

// 🕓 Жизненный цикл
onMounted(() => {
  loadInstructors();
  unsubscribe = onBalanceDone(() => loadInstructors(props.filters));

});
onUnmounted(() => {
  if (unsubscribe) unsubscribe();
});
watch(() => props.filters, loadInstructors, { deep: true });
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

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.hire-btn,
.fire-btn {
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  border: none;
  transition: background 0.2s, transform 0.1s;
}

.hire-btn {
  background: #4caf50;
}
.hire-btn:hover {
  background: #43a047;
  transform: scale(1.05);
}

.fire-btn {
  background: #f44336;
}
.fire-btn:hover {
  background: #e53935;
  transform: scale(1.05);
}

.table-wrapper {
  overflow-y: auto;
  max-height: 80vh;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-family: sans-serif;
}

th {
  background: #e3f2fd;
  padding: 8px;
  border-bottom: 1px solid #ccc;
  text-align: left;
}

td {
  padding: 8px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.checkbox-col {
  width: 40px;
  text-align: center;
}

input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.clickable {
  color: #1565c0;
  cursor: pointer;
  text-decoration: underline;
}
.clickable:hover {
  color: #0d47a1;
}

.loading,
.no-data {
  padding: 10px;
  text-align: center;
  color: #777;
}
</style>
