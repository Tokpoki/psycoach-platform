package com.psycoach.data.model

data class Scenario(
    val id: Int,
    val title: String,
    val role: String,
    val kind: String
)

data class Choice(
    val id: Int,
    val text: String,
    val explanation: String,
    val score_delta: Int
)

data class ScenarioDetail(
    val id: Int,
    val title: String,
    val description: String,
    val role: String,
    val kind: String,
    val choices: List<Choice>
)

data class ChoiceApplyRequest(
    val choice_id: Int
)

data class ChoiceApplyResponse(
    val result: String,
    val explanation: String,
    val score_delta: Int
)
