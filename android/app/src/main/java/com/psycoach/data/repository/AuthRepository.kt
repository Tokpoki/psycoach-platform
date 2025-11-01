package com.psycoach.data.repository

import android.util.Log
import com.psycoach.data.local.TokenStorage
import com.psycoach.data.model.AuthResponse
import com.psycoach.data.model.LoginRequest
import com.psycoach.data.model.RegisterRequest
import com.psycoach.data.remote.ApiService
import com.psycoach.domain.util.Result
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AuthRepository @Inject constructor(
    private val apiService: ApiService,
    private val tokenStorage: TokenStorage
) {
    suspend fun register(email: String, password: String, role: String): Result<AuthResponse> {
        return try {
            val response = apiService.register(RegisterRequest(email, password, role))
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) {
                    tokenStorage.saveToken(body.accessToken)
                    Result.Success(body)
                } else {
                    Result.Error("Empty response body while registering user.")
                }
            } else {
                val debugMessage = buildString {
                    append("Registration failed: HTTP ${response.code()}")
                    response.errorBody()?.string()?.takeIf { it.isNotBlank() }?.let { error ->
                        append(" – ")
                        append(error)
                    }
                }
                Log.e("AuthRepository", debugMessage)
                Result.Error(debugMessage)
            }
        } catch (e: Exception) {
            val message = "Unable to register: ${e.localizedMessage ?: e.javaClass.simpleName}"
            Log.e("AuthRepository", message, e)
            Result.Error(message, e)
        }
    }

    suspend fun login(email: String, password: String): Result<AuthResponse> {
        return try {
            val response = apiService.login(LoginRequest(email, password))
            if (response.isSuccessful) {
                val body = response.body()
                if (body != null) {
                    tokenStorage.saveToken(body.accessToken)
                    Result.Success(body)
                } else {
                    Result.Error("Empty response body while logging in.")
                }
            } else {
                val debugMessage = buildString {
                    append("Login failed: HTTP ${response.code()}")
                    response.errorBody()?.string()?.takeIf { it.isNotBlank() }?.let { error ->
                        append(" – ")
                        append(error)
                    }
                }
                Log.e("AuthRepository", debugMessage)
                Result.Error(debugMessage)
            }
        } catch (e: Exception) {
            val message = "Unable to login: ${e.localizedMessage ?: e.javaClass.simpleName}"
            Log.e("AuthRepository", message, e)
            Result.Error(message, e)
        }
    }

    fun getToken(): String? = tokenStorage.getToken()

    fun logout() {
        tokenStorage.clearToken()
    }
}
