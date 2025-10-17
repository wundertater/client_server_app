import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const url = error.config?.url;
    const data = error.response?.data;

    // === Игнорируем 404 при запросе фото ===
    if (url?.includes("/photo") && status === 404) {
      // Просто возвращаем Promise.reject без alert
      return Promise.reject(error);
    }

    // === Общая обработка остальных ошибок ===
    let message = "Ошибка при запросе";

    if (data) {
      if (typeof data.detail === "string") {
        message = data.detail;
      } else if (Array.isArray(data.detail)) {
        message = data.detail
          .map((err) => `${err.loc?.slice(-1)[0]}: ${err.msg}`)
          .join("\n");
      }
    }

    alert(message);
    return Promise.reject(error);
  }
);



// === Общие ===
export const getDepartments = () => api.get("/departments");
export const getGroups = () => api.get("/groups");

// === Преподаватели ===
export const getInstructorById = (instructor_id) =>
  api.get(`/instructors/${instructor_id}`);

export const getInstructors = (params) =>
  api.get("/instructors", {
    params,
    paramsSerializer: {
      serialize: (params) =>
        new URLSearchParams(
          Object.entries(params).flatMap(([key, val]) =>
            Array.isArray(val) ? val.map((v) => [key, v]) : [[key, val]]
          )
        ).toString(),
    },
  });

export const updateInstructor = (instructor_id, data) =>
  api.put(`/instructors/${instructor_id}/update`, data);

export const deleteInstructor = (instructor_id) =>
  api.delete(`/instructors/${instructor_id}/delete`);

export const addInstructor = (data) =>
  api.post(`/instructors/add`, data);

export const uploadInstructorPhoto = (id, file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post(`/instructors/${id}/photo`, formData);
};

export const getInstructorPhoto = async (id) => {
  const response = await api.get(`/instructors/${id}/photo`, {
    responseType: "blob",
  });
  return response.data;
};

// === Студенты ===
export const getStudentById = (student_id) =>
  api.get(`/students/${student_id}`);

export const getStudents = (params) =>
  api.get("/students", {
    params,
    paramsSerializer: {
      serialize: (params) =>
        new URLSearchParams(
          Object.entries(params).flatMap(([key, val]) =>
            Array.isArray(val) ? val.map((v) => [key, v]) : [[key, val]]
          )
        ).toString(),
    },
  });

export const updateStudent = (student_id, data) =>
  api.put(`/students/${student_id}/update`, data);

export const deleteStudent = (student_id) =>
  api.delete(`/students/${student_id}/delete`);

export const addStudent = (data) =>
  api.post(`/students/add`, data);

export const uploadStudentPhoto = (student_id, file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post(`/students/${student_id}/photo`, formData);
};

export const getStudentPhoto = async (id) => {
  const response = await api.get(`/students/${id}/photo`, {
    responseType: "blob",
  });
  return response.data;
};

export default api;
