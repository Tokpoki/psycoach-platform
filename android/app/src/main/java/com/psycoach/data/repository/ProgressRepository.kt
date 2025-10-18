package com.psycoach.data.repository

import com.psycoach.data.local.TokenStorage
import com.psycoach.data.model.MiniGameResultRequest
import com.psycoach.data.model.ProgressResponse
import com.psycoach.data.remote.ApiService
import com.psycoach.domain.util.Result
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ProgressRepository @Inject constructor(
    private val apiService: ApiService,
    private val tokenStorage: TokenStorage
) {
    suspend fun getProgress(): Result<ProgressResponse> {
        val token = tokenStorage.getToken() ?: return Result.Error("Token missing")
        return try {
            val response = apiService.getProgress("Bearer $token")
            if (response.isSuccessful) {
                response.body()?.let { Result.Success(it) } ?: Result.Error("Empty response body")
            } else {
                Result.Error("Failed to load progress: ${response.code()}")
            }
        } catch (e: Exception) {
            Result.Error("Unable to load progress", e)
        }
    }

    suspend fun sendMiniGameResult(type: String, score: Int): Result<ProgressResponse> {
        val token = tokenStorage.getToken() ?: return Result.Error("Token missing")
        return try {
            val response = apiService.sendMiniGameResult(
                token = "Bearer $token",
                type = type,
                body = MiniGameResultRequest(score)
            )
            if (response.isSuccessful) {
                response.body()?.let { Result.Success(it) } ?: Result.Error("Empty response body")
            } else {
                Result.Error("Failed to send result: ${response.code()}")
            }
        } catch (e: Exception) {
            Result.Error("Unable to send result", e)
        }
    }
}
