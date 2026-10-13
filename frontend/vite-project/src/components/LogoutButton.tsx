import Button from "@mui/material/Button";

export default function LogoutButton() {

  const logout = () => {

    localStorage.clear();

    window.location.reload();
  };

  return (
    <Button
      variant="outlined"
      color="error"
      onClick={logout}
    >
      Logout
    </Button>
  );
}