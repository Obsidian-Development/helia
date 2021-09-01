/*
 * This Kotlin source file was generated by the Gradle 'init' task.
 */
package helia

import com.kotlindiscord.kord.extensions.ExtensibleBot
import com.kotlindiscord.kord.extensions.utils.env
import dev.kord.common.entity.PresenceStatus
import dev.kord.common.entity.Snowflake

import helia.extensions.KickCommandH
import helia.extensions.BanCommandH
import helia.extensions.GuildCommandH

val TEST_SERVER_ID = Snowflake(
    env("TEST_SERVER")?.toLong()  // Get the test server ID from the env vars or a .env file
        ?: error("Env var TEST_SERVER not provided")
)

private val TOKEN = env("TOKEN")   // Get the bot' token from the env vars or a .env file
    ?: error("Env var TOKEN not provided")

suspend fun main() {
    val bot = ExtensibleBot(TOKEN) {
        messageCommands {
            defaultPrefix = "?"

            prefix { default ->
                if (guildId == TEST_SERVER_ID) {
                    // For the test server, we use ! as the command prefix
                    "!"
                } else {
                    // For other servers, we use the configured default prefix
                    default
                }
            }
        }

        slashCommands {
            enabled = true
        }

        extensions {
            add(::KickCommandH)
            add(::BanCommandH)
            add(::GuildCommandH)
        }
        presence {
            status = PresenceStatus.Online
            playing("Kotlin beginings")
        }
    }

    bot.start()
}
