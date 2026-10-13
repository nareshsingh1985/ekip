import {
  Paper,
  Typography,
} from "@mui/material";

export default function UserInfo() {

  const username =
    localStorage.getItem("user");

  const role =
    localStorage.getItem("role");

  return (
    <Paper sx={{ p: 2, mb: 3 }}>
      <Typography>
        User: {username}
      </Typography>

      <Typography>
        Role: {role}
      </Typography>
    </Paper>
  );
}