package com.psycoach.ui.screen.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.psycoach.data.model.AuthResponse
import com.psycoach.domain.util.Result

@Composable
fun LoginScreen(
    authState: Result<AuthResponse>?,
    onLogin: (String, String) -> Unit,
    onRegister: (String, String, String) -> Unit,
    onNavigateToScenarios: () -> Unit
) {
    val emailState = remember { mutableStateOf("") }
    val passwordState = remember { mutableStateOf("") }
    val roleState = remember { mutableStateOf("athlete") }

    LaunchedEffect(authState) {
        if (authState is Result.Success) {
            onNavigateToScenarios()
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(text = "Добро пожаловать в PsyCoach", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(24.dp))
        OutlinedTextField(
            value = emailState.value,
            onValueChange = { emailState.value = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth(),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email)
        )
        Spacer(modifier = Modifier.height(12.dp))
        OutlinedTextField(
            value = passwordState.value,
            onValueChange = { passwordState.value = it },
            label = { Text("Пароль") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation()
        )
        Spacer(modifier = Modifier.height(12.dp))
        OutlinedTextField(
            value = roleState.value,
            onValueChange = { roleState.value = it },
            label = { Text("Роль (например, athlete)") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(24.dp))
        if (authState is Result.Loading) {
            CircularProgressIndicator()
        } else {
            Button(
                onClick = { onLogin(emailState.value, passwordState.value) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Login")
            }
            Spacer(modifier = Modifier.height(12.dp))
            Button(
                onClick = { onRegister(emailState.value, passwordState.value, roleState.value) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Register")
            }
            if (authState is Result.Error) {
                Spacer(modifier = Modifier.height(12.dp))
                Text(text = authState.message, color = MaterialTheme.colorScheme.error)
            }
        }
    }
}
