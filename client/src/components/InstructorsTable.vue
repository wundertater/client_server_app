<template>
  <div class="instructors-table">
    <h3>Преподаватели</h3>

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
          <h3>Редактирование преподавателя</h3>

          <div v-if="modalLoading" class="loading">Загрузка...</div>

          <div v-else-if="form" class="instructor-card">
            <div class="photo-block">
              <div
                v-if="photoPreview"
                class="photo"
                :style="{ backgroundImage: `url(${photoPreview})` }"
              ></div>
              <div v-else class="photo placeholder">Нет фото</div>

              <input type="file" accept="image/*" @change="onPhotoSelected" />
            </div>

            <div class="info">
              <label>Имя:</label>
              <input v-model="form.first_name" type="text" />

              <label>Фамилия:</label>
              <input v-model="form.last_name" type="text" />

              <label>Дата рождения:</label>
              <input v-model="form.birth_date" type="date" />

              <label>Дата приёма:</label>
              <input v-model="form.employ_date" type="date" />

              <label>ID кафедры:</label>
              <input v-model.number="form.department_id" type="number" />
            </div>

            <div class="buttons">
              <button class="save-btn" @click="applyUpdate">Применить</button>
              <button class="close-btn" @click="closeModal">Отмена</button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { onBalanceDone } from "@/websocket";
import { getInstructors, getInstructorById, updateInstructor } from "@/api";

let unsubscribe = null;

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
const form = ref(null);
const selectedId = ref(null);
const photoPreview = ref(null);

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
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const openInstructor = async (id) => {
  showModal.value = true;
  modalLoading.value = true;
  form.value = null;
  photoPreview.value = null;
  selectedId.value = id;

  try {
    const { data } = await getInstructorById(id);
    form.value = {
      first_name: data.first_name,
      last_name: data.last_name,
      birth_date: data.birth_date,
      employ_date: data.employ_date,
      department_id: data.department_id,
      photo: data.photo,
    };

    if (data.photo) {
      const byteArray = new Uint8Array(data.photo);
      const blob = new Blob([byteArray], { type: "image/jpeg" });
      photoPreview.value = URL.createObjectURL(blob);
    }
  } catch (err) {
    console.error("Ошибка загрузки преподавателя:", err);
  } finally {
    modalLoading.value = false;
  }
};

const onPhotoSelected = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    form.value.photo = e.target.result.split(",")[1]; // base64 без префикса
    photoPreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

const applyUpdate = async () => {
  try {
    const payload = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      birth_date: form.value.birth_date,
      department_id: form.value.department_id,
      photo: form.value.photo,
    };

    await updateInstructor(selectedId.value, payload);
    alert("Данные преподавателя успешно обновлены!");
    await loadInstructors(); // обновляем таблицу
    closeModal();
  } catch (err) {
    console.error("Ошибка обновления преподавателя:", err);
    alert("Ошибка при сохранении изменений");
  }
};

const closeModal = () => {
  showModal.value = false;
  form.value = null;
  photoPreview.value = null;
};

onMounted(() => {
  loadInstructors();
  unsubscribe = onBalanceDone(loadInstructors);
});

onUnmounted(() => {
  // Отписываемся при уничтожении компонента
  if (unsubscribe) unsubscribe();
});

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

/* --- Модалка --- */
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
  width: 380px;
  max-width: 90%;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
}

.instructor-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.photo-block {
  width: 150px;
  height: 150px;
  margin-bottom: 10px;
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
  border-radius: 50%;
}

.info {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 14px;
  color: #333;
}

input {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.buttons {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.save-btn {
  flex: 1;
  background: #4caf50;
  color: white;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.save-btn:hover {
  background: #43a047;
}

.close-btn {
  flex: 1;
  background: #f44336;
  color: white;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.close-btn:hover {
  background: #e53935;
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
