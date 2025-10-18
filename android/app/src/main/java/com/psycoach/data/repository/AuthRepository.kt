package com.psycoach.data.repository

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
                    Result.Error("Empty response body")
                }
            } else {
                Result.Error("Registration failed: ${response.code()}")
            }
        } catch (e: Exception) {
            Result.Error("Unable to register", e)
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
                    Result.Error("Empty response body")
                }
            } else {
                Result.Error("Login failed: ${response.code()}")
            }
        } catch (e: Exception) {
            Result.Error("Unable to login", e)
        }
    }

    fun getToken(): String? = tokenStorage.getToken()

    fun logout() {
        tokenStorage.clearToken()
    }
}
