<template>
  <transition name="fade">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-card">
        <h3>Карточка {{ type === 'instructor' ? 'преподавателя' : 'студента' }}</h3>

        <div class="photo-section">
          <div
            v-if="photoPreview"
            class="photo"
            :style="{ backgroundImage: `url(${photoPreview})` }"
          ></div>
          <div v-else class="photo placeholder">
            <span>Нет фото</span>
          </div>
          <input type="file" accept="image/*" @change="onPhotoSelected" />
        </div>

        <div class="form">
          <label>Фамилия:</label>
          <input v-model="form.last_name" type="text" placeholder="Введите фамилию" />

          <label>Имя:</label>
          <input v-model="form.first_name" type="text" placeholder="Введите имя" />

          <label>Дата рождения:</label>
          <input v-model="form.birth_date" type="date" />

          <label>Кафедра:</label>
          <select v-model.number="form.department_id">
            <option disabled value="">Выберите кафедру</option>
            <option
              v-for="dep in departments"
              :key="dep.id"
              :value="dep.id"
            >
              {{ dep.name }}
            </option>
          </select>
        </div>

        <div class="buttons">
          <button class="ok-btn" @click="handleSave">Ок</button>
          <button class="cancel-btn" @click="close">Отмена</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  getDepartments,
  addStudent,
  uploadStudentPhoto,
  addInstructor,
  uploadInstructorPhoto,
} from "@/api";

const props = defineProps({
  visible: Boolean,
  type: { type: String, default: "student" }, // 'student' | 'instructor'
});

const emit = defineEmits(["close", "save"]);

const form = ref({
  last_name: "",
  first_name: "",
  birth_date: "",
  department_id: "",
});
const departments = ref([]);
const selectedPhoto = ref(null);
const photoPreview = ref(null);

// Загрузка кафедр
const loadDepartments = async () => {
  try {
    const { data } = await getDepartments();
    departments.value = data;
  } catch (err) {
    console.error("Ошибка загрузки кафедр:", err);
  }
};

// Выбор фото
const onPhotoSelected = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  selectedPhoto.value = file;

  const reader = new FileReader();
  reader.onload = (event) => {
    photoPreview.value = event.target.result;
  };
  reader.readAsDataURL(file);
};

// Сохранение
const handleSave = async () => {
  if (!form.value.last_name || !form.value.first_name || !form.value.department_id) {
    alert("Пожалуйста, заполните все обязательные поля.");
    return;
  }

  try {
    let id = null;

    if (props.type === "student") {
      const { data } = await addStudent(form.value);
      id = data?.id;
      if (selectedPhoto.value && id) {
        await uploadStudentPhoto(id, selectedPhoto.value);
      }
    } else {
      const { data } = await addInstructor(form.value);
      id = data?.id;
      if (selectedPhoto.value && id) {
        await uploadInstructorPhoto(id, selectedPhoto.value);
      }
    }

    emit("save");
    close();
  } catch (err) {
    console.error("Ошибка при сохранении:", err);
  }
};

const close = () => emit("close");

onMounted(loadDepartments);
</script>

<style scoped>
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
  padding: 20px 24px;
  width: 380px;
  max-width: 90%;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
}

h3 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
}

.photo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;
}

.photo {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px solid #ccc;
  background-size: cover;
  background-position: center;
  margin-bottom: 6px;
}

.placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f2f2f2;
  color: #888;
  font-size: 13px;
}

.form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

label {
  font-weight: 500;
  font-size: 14px;
  color: #333;
}

input,
select {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.buttons {
  display: flex;
  gap: 10px;
  width: 100%;
}

.ok-btn,
.cancel-btn {
  flex: 1;
  padding: 8px;
  border-radius: 6px;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}

.ok-btn {
  background: #4caf50;
  color: white;
}
.ok-btn:hover {
  background: #43a047;
}

.cancel-btn {
  background: #f44336;
  color: white;
}
.cancel-btn:hover {
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
