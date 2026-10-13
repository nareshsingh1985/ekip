export const getRole = () => {
  return localStorage.getItem("role");
};

export const isAdmin = () =>
  getRole() === "Admin";

export const isKnowledgeManager =
  () =>
    getRole() ===
    "Knowledge Manager";

export const isBusinessUser =
  () =>
    getRole() ===
    "Business User";

export const isExecutive = () =>
  getRole() === "Executive";