package com.psycoach.data.remote

import com.psycoach.data.model.AuthResponse
import com.psycoach.data.model.ChoiceApplyRequest
import com.psycoach.data.model.ChoiceApplyResponse
import com.psycoach.data.model.LoginRequest
import com.psycoach.data.model.MiniGameResultRequest
import com.psycoach.data.model.ProgressResponse
import com.psycoach.data.model.RegisterRequest
import com.psycoach.data.model.Scenario
import com.psycoach.data.model.ScenarioDetail
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface ApiService {
    @POST("auth/register")
    suspend fun register(@Body body: RegisterRequest): Response<AuthResponse>

    @POST("auth/login")
    suspend fun login(@Body body: LoginRequest): Response<AuthResponse>

    @GET("scenarios")
    suspend fun getScenarios(
        @Header("Authorization") token: String,
        @Query("role") role: String?,
        @Query("kind") kind: String?
    ): Response<List<Scenario>>

    @GET("scenarios/{id}")
    suspend fun getScenarioById(
        @Header("Authorization") token: String,
        @Path("id") id: Int
    ): Response<ScenarioDetail>

    @POST("scenarios/{id}/choice")
    suspend fun chooseOption(
        @Header("Authorization") token: String,
        @Path("id") id: Int,
        @Body body: ChoiceApplyRequest
    ): Response<ChoiceApplyResponse>

    @POST("minigames/{type}/result")
    suspend fun sendMiniGameResult(
        @Header("Authorization") token: String,
        @Path("type") type: String,
        @Body body: MiniGameResultRequest
    ): Response<ProgressResponse>

    @GET("progress/me")
    suspend fun getProgress(
        @Header("Authorization") token: String
    ): Response<ProgressResponse>
}
