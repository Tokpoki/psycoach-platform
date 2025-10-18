package com.psycoach.data.repository

import com.psycoach.data.local.TokenStorage
import com.psycoach.data.model.ChoiceApplyRequest
import com.psycoach.data.model.ChoiceApplyResponse
import com.psycoach.data.model.Scenario
import com.psycoach.data.model.ScenarioDetail
import com.psycoach.data.remote.ApiService
import com.psycoach.domain.util.Result
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ScenarioRepository @Inject constructor(
    private val apiService: ApiService,
    private val tokenStorage: TokenStorage
) {
    suspend fun getScenarios(role: String?, kind: String?): Result<List<Scenario>> {
        val token = tokenStorage.getToken() ?: return Result.Error("Token missing")
        return try {
            val response = apiService.getScenarios("Bearer $token", role, kind)
            if (response.isSuccessful) {
                response.body()?.let { Result.Success(it) } ?: Result.Error("Empty response body")
            } else {
                Result.Error("Failed to load scenarios: ${response.code()}")
            }
        } catch (e: Exception) {
            Result.Error("Unable to load scenarios", e)
        }
    }

    suspend fun getScenarioById(id: Int): Result<ScenarioDetail> {
        val token = tokenStorage.getToken() ?: return Result.Error("Token missing")
        return try {
            val response = apiService.getScenarioById("Bearer $token", id)
            if (response.isSuccessful) {
                response.body()?.let { Result.Success(it) } ?: Result.Error("Empty response body")
            } else {
                Result.Error("Failed to load scenario: ${response.code()}")
            }
        } catch (e: Exception) {
            Result.Error("Unable to load scenario", e)
        }
    }

    suspend fun chooseOption(scenarioId: Int, choiceId: Int): Result<ChoiceApplyResponse> {
        val token = tokenStorage.getToken() ?: return Result.Error("Token missing")
        return try {
            val response = apiService.chooseOption(
                token = "Bearer $token",
                id = scenarioId,
                body = ChoiceApplyRequest(choice_id = choiceId)
            )
            if (response.isSuccessful) {
                response.body()?.let { Result.Success(it) } ?: Result.Error("Empty response body")
            } else {
                Result.Error("Failed to submit choice: ${response.code()}")
            }
        } catch (e: Exception) {
            Result.Error("Unable to submit choice", e)
        }
    }
}
