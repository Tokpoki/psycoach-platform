package com.psycoach.data.model

data class ProgressResponse(
    val score: Int,
    val level: Int,
    val badges: List<String>
)

data class MiniGameResultRequest(
    val score: Int
)
