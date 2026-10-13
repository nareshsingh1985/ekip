import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Stack,
} from "@mui/material";

import { useState } from "react";

import { login } from "../api/authApi";

interface Props {
  onLogin: () => void;
}

export default function LoginPage({
  onLogin,
}: Props) {

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const handleLogin = async () => {

    const result =
      await login(
        username,
        password
      );

    if (result.success) {

      localStorage.setItem(
        "user",
        username
        );

        localStorage.setItem(
        "role",
        result.role
        );

      onLogin();
    }
  };

  return (
    <Container maxWidth="sm">

      <Paper sx={{ p: 4, mt: 10 }}>

        <Typography
          variant="h4"
          gutterBottom
        >
          EKIP Login
        </Typography>

        <Stack spacing={2}>

          <TextField
            label="Username"
            value={username}
            onChange={(e) =>
              setUsername(
                e.target.value
              )
            }
          />

          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          <Button
            variant="contained"
            onClick={handleLogin}
          >
            Login
          </Button>

        </Stack>

      </Paper>

    </Container>
  );
}