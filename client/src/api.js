import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const getDepartments = () => api.get("/departments/");
export const getGroups = () => api.get("/groups/");
export const getInstructorById = (instructor_id) =>
  api.get(`/instructors/${instructor_id}/`);
export const getInstructors = (params) => api.get("/instructors/", { params });
export const updateInstructor = (instructor_id, data) =>
  api.put(`/instructors/${instructor_id}/update/`, data);

export default api;