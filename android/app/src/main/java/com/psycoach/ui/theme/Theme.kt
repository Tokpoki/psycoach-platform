package com.psycoach.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = RoyalPurple,
    onPrimary = Color.White,
    background = DeepBlue,
    onBackground = SoftWhite,
    secondary = Lavender
)

private val LightColorScheme = lightColorScheme(
    primary = RoyalPurple,
    onPrimary = Color.White,
    background = SoftWhite,
    onBackground = DeepBlue,
    secondary = Lavender
)

@Composable
fun PsyCoachTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
