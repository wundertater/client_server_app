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
            <td class="clickable" @click="openInstructor(inst.id)">
              {{ inst.first_name }} {{ inst.last_name }}
            </td>
            <td>{{ inst.department?.name || "-" }}</td>
            <td>{{ inst.groups.join(", ") }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно -->
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-card">
          <h3>Карточка преподавателя</h3>

          <div v-if="modalLoading" class="loading">Загрузка...</div>

          <div v-else-if="selectedInstructor" class="instructor-card">
            <div class="photo-block">
              <div
                v-if="photoUrl"
                class="photo"
                :style="{ backgroundImage: `url(${photoUrl})` }"
              ></div>
              <div v-else class="photo placeholder">Нет фото</div>
            </div>

            <div class="info">
              <p><strong>Имя:</strong> {{ selectedInstructor.first_name }}</p>
              <p><strong>Фамилия:</strong> {{ selectedInstructor.last_name }}</p>
              <p><strong>Дата рождения:</strong> {{ selectedInstructor.birth_date }}</p>
              <p><strong>Дата приема:</strong> {{ selectedInstructor.employ_date }}</p>
              <p><strong>Кафедра ID:</strong> {{ selectedInstructor.department_id }}</p>
            </div>

            <button class="close-btn" @click="closeModal">Закрыть</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { getInstructors, getInstructorById } from "@/api";

const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
});

const instructors = ref([]);
const loading = ref(false);

const showModal = ref(false);
const modalLoading = ref(false);
const selectedInstructor = ref(null);
const photoUrl = ref(null);

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
  } catch (err) {
    console.error("Ошибка загрузки преподавателей:", err);
  } finally {
    loading.value = false;
  }
};

const openInstructor = async (id) => {
  showModal.value = true;
  modalLoading.value = true;
  selectedInstructor.value = null;
  photoUrl.value = null;

  try {
    const { data } = await getInstructorById(id);
    selectedInstructor.value = data;

    if (data.photo) {
      // фото — это массив байт, превращаем в Blob URL
      const byteArray = new Uint8Array(data.photo);
      const blob = new Blob([byteArray], { type: "image/jpeg" });
      photoUrl.value = URL.createObjectURL(blob);
    }
  } catch (err) {
    console.error("Ошибка загрузки преподавателя:", err);
  } finally {
    modalLoading.value = false;
  }
};

const closeModal = () => {
  showModal.value = false;
  selectedInstructor.value = null;
  photoUrl.value = null;
};

// загружаем преподавателей при старте
onMounted(() => loadInstructors());

// обновляем при изменении фильтров
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
  text-align: center;
  padding: 20px;
  color: #555;
}

/* --- Модальное окно --- */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  width: 350px;
  max-width: 90%;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
}

.instructor-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.photo-block {
  width: 150px;
  height: 150px;
  margin-bottom: 15px;
}

.photo {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 50%;
  border: 2px solid #ccc;
}

.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  color: #888;
  font-size: 14px;
}

.info {
  text-align: left;
  width: 100%;
}

.close-btn {
  margin-top: 16px;
  padding: 8px 12px;
  border: none;
  background: #2196f3;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}

.close-btn:hover {
  background: #1976d2;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
