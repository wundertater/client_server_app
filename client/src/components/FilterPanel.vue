<template>
  <div class="filter-panel">
    <transition name="fade">
      <div v-if="showFilters" class="filters">
        <!-- Кафедры -->
        <div class="filter-block">
          <div class="dropdown-header" @click="toggleDepartments">
            <span>Кафедра</span>
            <span>{{ showDepartments ? "▲" : "▼" }}</span>
          </div>
          <div v-if="showDepartments" class="dropdown-content">
            <div
              v-for="dept in departments"
              :key="dept.id"
              class="checkbox-item"
            >
              <input
                type="checkbox"
                :id="'dept-' + dept.id"
                :value="dept.id"
                v-model="selectedDepartments"
              />
              <label :for="'dept-' + dept.id">{{ dept.name }}</label>
            </div>
          </div>
        </div>

        <!-- Группы -->
        <div class="filter-block">
          <div class="dropdown-header" @click="toggleGroups">
            <span>Группы</span>
            <span>{{ showGroups ? "▲" : "▼" }}</span>
          </div>
          <div v-if="showGroups" class="dropdown-content">
            <div v-for="group in groups" :key="group.id" class="checkbox-item">
              <input
                type="checkbox"
                :id="'group-' + group.id"
                :value="group.id"
                v-model="selectedGroups"
              />
              <label :for="'group-' + group.id">{{ group.id }}</label>
            </div>
          </div>
        </div>

        <!-- ФИ -->
        <div class="filter-block">
          <input v-model="filters.lastName" placeholder="Фамилия" />
          <input v-model="filters.firstName" placeholder="Имя" />
        </div>

        <!-- Кнопка -->
        <button class="apply-btn" @click="applyFilters">Применить</button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { getDepartments, getGroups } from "@/api";
import { onBalanceDone } from "@/websocket";

const showFilters = ref(true);
const showDepartments = ref(true);
const showGroups = ref(true);

const departments = ref([]);
const groups = ref([]);
const emit = defineEmits(["apply-filters"]);

const selectedDepartments = ref([]);
const selectedGroups = ref([]);

const filters = ref({
  firstName: "",
  lastName: "",
});

const toggleDepartments = () => (showDepartments.value = !showDepartments.value);
const toggleGroups = () => (showGroups.value = !showGroups.value);

// === 🔁 Обновление групп ===
async function reloadGroups() {
  try {
    const res = await getGroups();
    groups.value = res.data;
    console.log("Группы обновлены:", groups.value);
  } catch (err) {
    console.error("Ошибка при обновлении групп:", err);
  }
}

let unsubscribe = null;

onMounted(async () => {
  try {
    const [deptRes, groupRes] = await Promise.all([
      getDepartments(),
      getGroups(),
    ]);
    departments.value = deptRes.data;
    groups.value = groupRes.data;
  } catch (err) {
    console.error("Ошибка загрузки данных:", err);
  }

  // Подписываемся на websocket-событие
  unsubscribe = onBalanceDone(() => {
    console.log("Сообщение по websocket: обновляем группы...");
    reloadGroups();
  });
});

onBeforeUnmount(() => {
  // Отписываемся от сокета, чтобы не было утечек
  if (unsubscribe) unsubscribe();
});

const applyFilters = () => {
  const payload = {
    departments: selectedDepartments.value,
    groups: selectedGroups.value,
    ...filters.value,
  };
  emit("apply-filters", payload);
};
</script>

<style scoped>
.filter-panel {
  background: linear-gradient(to bottom, #b5dcf9, #e9f6ff);
  border-radius: 12px;
  padding: 10px;
  font-family: sans-serif;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.15);
}

.filter-block {
  margin-top: 10px;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #e0f2ff;
  border-radius: 6px;
  padding: 5px;
  cursor: pointer;
}

.dropdown-content {
  max-height: 150px;
  overflow-y: auto;
  margin-top: 5px;
  background: white;
  border-radius: 6px;
  border: 1px solid #ccc;
  padding: 5px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

input[type="text"],
input[type="checkbox"] {
  cursor: pointer;
}

input[type="text"] {
  width: 100%;
  margin-top: 6px;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 5px;
}

.apply-btn {
  width: 100%;
  margin-top: 12px;
  padding: 8px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.apply-btn:hover {
  background-color: #43a047;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
