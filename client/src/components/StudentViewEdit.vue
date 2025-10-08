<template>
  <transition name="fade">
    <div class="modal-overlay" @click.self="emit('close')">
      <div class="modal-card">
        <h3>Карточка студента</h3>

        <div v-if="loading" class="loading">Загрузка...</div>

        <div v-else-if="form" class="student-card">
          <!-- 🖼 Фото -->
          <div class="photo-block">
            <div
              v-if="photoPreview"
              class="photo"
              :style="{ backgroundImage: `url(${photoPreview})` }"
            ></div>
            <div v-else class="photo placeholder">Нет фото</div>

            <input type="file" accept="image/*" @change="onPhotoSelected" />
          </div>

          <!-- 👤 Основные данные -->
          <div class="info">
            <label>Имя:</label>
            <input v-model="form.first_name" type="text" />

            <label>Фамилия:</label>
            <input v-model="form.last_name" type="text" />

            <label>Дата рождения:</label>
            <input v-model="form.birth_date" type="date" />

            <label>Дата зачисления:</label>
            <input v-model="form.enroll_date" type="date" />

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

          <!-- 📊 Таблица оценок -->
          <div class="marks-section">
            <h4>Оценки по предметам</h4>
            <table class="marks-table">
              <thead>
                <tr>
                  <th>Предмет</th>
                  <th>Оценка</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, index) in form.student_subjects"
                  :key="item.subject.id"
                >
                  <td>{{ item.subject.name }}</td>
                  <td>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      v-model.number="form.student_subjects[index].mark"
                      placeholder="Введите оценку"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 🔘 Кнопки -->
          <div class="buttons">
            <button class="save-btn" @click="applyUpdate">Сохранить</button>
            <button class="close-btn" @click="emit('close')">Отмена</button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  getStudentById,
  updateStudent,
  getStudentPhoto,
  uploadStudentPhoto,
  getDepartments,
} from "@/api";

const props = defineProps({
  studentId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["close", "updated"]);

const form = ref(null);
const loading = ref(false);
const photoPreview = ref(null);
const selectedPhoto = ref(null);
const departments = ref([]);

// === Загрузка данных студента ===
const loadStudent = async () => {
  loading.value = true;
  try {
    const { data } = await getStudentById(props.studentId);
    form.value = { ...data };

    // 📸 загружаем фото отдельно
    try {
      const photoBlob = await getStudentPhoto(props.studentId);
      photoPreview.value = URL.createObjectURL(photoBlob);
    } catch {
      photoPreview.value = null;
    }
  } catch (err) {
    console.error("Ошибка загрузки студента:", err);
  } finally {
    loading.value = false;
  }
};

// === Загрузка кафедр ===
const loadDepartments = async () => {
  try {
    const { data } = await getDepartments();
    departments.value = data;
  } catch (err) {
    console.error("Ошибка загрузки кафедр:", err);
  }
};

// === Выбор нового фото ===
const onPhotoSelected = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  selectedPhoto.value = file;

  const reader = new FileReader();
  reader.onload = (ev) => {
    photoPreview.value = ev.target.result;
  };
  reader.readAsDataURL(file);
};

// === Сохранение изменений ===
const applyUpdate = async () => {
  try {
    const marksPayload = {};
    for (const item of form.value.student_subjects) {
      marksPayload[item.subject.id] = item.mark ?? 0;
    }

    const payload = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      birth_date: form.value.birth_date,
      enroll_date: form.value.enroll_date,
      department_id: form.value.department_id,
      marks: marksPayload,
    };

    await updateStudent(props.studentId, payload);

    // если выбрано новое фото — обновляем его отдельно
    if (selectedPhoto.value) {
      await uploadStudentPhoto(props.studentId, selectedPhoto.value);
    }

    alert("✅ Данные студента успешно обновлены!");
    emit("updated");
    emit("close");
  } catch (err) {
    console.error("Ошибка обновления студента:", err);
    alert("Ошибка при сохранении изменений");
  }
};

onMounted(async () => {
  await loadDepartments();
  await loadStudent();
});
</script>


<style scoped>
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
  width: 480px;
  max-width: 95%;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
}

.student-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.photo-block {
  width: 140px;
  height: 140px;
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

.marks-section {
  width: 100%;
  margin-top: 12px;
}

.marks-section h4 {
  margin-bottom: 6px;
  text-align: left;
  color: #333;
}

.marks-table {
  width: 100%;
  border-collapse: collapse;
}

.marks-table th,
.marks-table td {
  border: 1px solid #ddd;
  padding: 6px;
  text-align: left;
}

.marks-table input {
  width: 100%;
  padding: 4px;
  border-radius: 4px;
  border: 1px solid #ccc;
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

.loading {
  text-align: center;
  color: #777;
}
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  overflow-y: auto; /* чтобы при переполнении появлялся скролл */
  padding: 20px;    /* отступы от краев экрана */
}

.modal-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  width: 380px;
  max-width: 90%;
  max-height: 90vh; /* ограничиваем высоту до 90% окна */
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.3);
  overflow-y: auto; /* прокрутка внутри модалки */
}

</style>
