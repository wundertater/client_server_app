<template>
  <div class="students-table">
    <div class="header-row">
      <h3>Студенты</h3>

      <!-- Кнопки действий -->
      <div class="action-buttons">
        <button class="enroll-btn" @click="openAddModal">Зачислить</button>
        <button class="expel-btn" @click="expelSelected">Отчислить</button>
      </div>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="students.length === 0" class="no-data">Нет данных</div>

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
            <th>Группа</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student.id">
            <td class="checkbox-col">
              <input type="checkbox" v-model="selectedIds" :value="student.id" />
            </td>
            <td class="clickable" @click="openStudent(student.id)">
              {{ student.first_name }} {{ student.last_name }}
            </td>
            <td>{{ student.department?.name || "-" }}</td>
            <td>{{ student.group ?? "-" }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 🔍 Модалка просмотра студента (пока заглушка) -->
    <StudentViewEdit
  v-if="showModal"
  :studentId="selectedId"
  @close="closeModal"
  @updated="handleStudentUpdated"
/>


    <!-- 🟢 Модалка добавления студента -->
    <AddPersonModal
  v-if="showAddModal"
  :visible="showAddModal"
  type="student"
  @close="showAddModal = false"
  @save="handleStudentAdded"
/>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { onBalanceDone } from "@/websocket";
import StudentViewEdit from "./StudentViewEdit.vue";
import {
  getStudents,
  deleteStudent,
  addStudent,
} from "@/api";
import AddPersonModal from "./AddPersonModal.vue";

const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
});

const students = ref([]);
const loading = ref(false);
const showModal = ref(false);
const selectedId = ref(null);
const selectedIds = ref([]);
const showAddModal = ref(false);

let unsubscribe = null;

// 📥 Загрузка студентов
const loadStudents = async (filters = {}) => {
  loading.value = true;
  try {
    const params = {};
    if (filters.departments?.length) params.d = filters.departments;
    if (filters.groups?.length) params.g = filters.groups;
    if (filters.firstName) params.fn = filters.firstName;
    if (filters.lastName) params.ln = filters.lastName;

    const { data } = await getStudents(params);
    students.value = data;
    selectedIds.value = [];
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleStudentAdded = async () => {
  alert("Студент успешно добавлен!");
  showAddModal.value = false;
};


// 👤 Просмотр/редактирование
const openStudent = (id) => {
  selectedId.value = id;
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
  selectedId.value = null;
};
const handleStudentUpdated = async () => {
  await loadStudents(props.filters);
};

// ➕ Открытие/закрытие модалки добавления
const openAddModal = () => {
  showAddModal.value = true;
};
const closeAddModal = () => {
  showAddModal.value = false;
};

// 💾 Добавление нового студента
const handleAddStudent = async (formData) => {
  try {
    await addStudent(formData);
    alert("Студент успешно зачислен!");
    showAddModal.value = false;
    await loadStudents(props.filters);
  } catch (err) {
    console.error("Ошибка при добавлении студента:", err);
    alert("Ошибка при добавлении студента.");
  }
};

// 🔘 Работа с чекбоксами
const allSelected = computed(
  () =>
    students.value.length > 0 &&
    selectedIds.value.length === students.value.length
);

const toggleSelectAll = () => {
  if (allSelected.value) selectedIds.value = [];
  else selectedIds.value = students.value.map((s) => s.id);
};

// 🔥 Отчисление выбранных студентов
const expelSelected = async () => {
  if (selectedIds.value.length === 0) {
    alert("Выберите хотя бы одного студента для отчисления.");
    return;
  }

  if (!confirm("Вы действительно хотите отчислить выбранных студентов?")) {
    return;
  }

  const failed = [];
  for (const id of selectedIds.value) {
    const student = students.value.find((s) => s.id === id);
    try {
      await deleteStudent(id);
    } catch (err) {
      failed.push(`${student?.first_name || ""} ${student?.last_name || ""}`.trim());
    }
  }

  if (failed.length > 0) {
    alert(`Не удалось отчислить: ${failed.join(", ")}`);
  } else {
    alert("Выбранные студенты успешно отчислены!");
  }

  await loadStudents(props.filters);
};

// 🔁 Инициализация
onMounted(() => {
  loadStudents();
  unsubscribe = onBalanceDone(() => loadStudents(props.filters));

});
onUnmounted(() => {
  if (unsubscribe) unsubscribe();
});
watch(() => props.filters, loadStudents, { deep: true });
</script>

<style scoped>
.students-table {
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

.enroll-btn,
.expel-btn {
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  border: none;
  transition: background 0.2s, transform 0.1s;
}

.enroll-btn {
  background: #4caf50;
}
.enroll-btn:hover {
  background: #43a047;
  transform: scale(1.05);
}

.expel-btn {
  background: #f44336;
}
.expel-btn:hover {
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

/* Заглушка для модалки просмотра */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  width: 320px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
  text-align: center;
}
.close-btn {
  margin-top: 16px;
  padding: 8px 14px;
  border: none;
  background: #1976d2;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
}
.close-btn:hover {
  background: #1565c0;
}
</style>
