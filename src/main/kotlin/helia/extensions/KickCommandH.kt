package helia.extensions

import com.kotlindiscord.kord.extensions.checks.hasPermission
import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingCoalescingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.member
import com.kotlindiscord.kord.extensions.commands.converters.impl.user
import com.kotlindiscord.kord.extensions.commands.parser.Arguments
import com.kotlindiscord.kord.extensions.commands.slash.AutoAckType
import com.kotlindiscord.kord.extensions.extensions.Extension
import com.kotlindiscord.kord.extensions.utils.respond
import dev.kord.common.annotation.KordPreview
import dev.kord.common.entity.Permission
import dev.kord.rest.builder.message.create.embed

import helia.TEST_SERVER_ID


@OptIn(KordPreview::class)
class KickCommandH : Extension() {
    override val name = "kick"


    override suspend fun setup() {
        command(::kickArgs) {
            name = "kick"
            description = "Ask the bot to kick a user"



            check { hasPermission(Permission.KickMembers); message= "You are missing the required permissions"  }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@KickCommandH.kord

                // Don't kick ourselves on request, kick the requested user!
                val realTarget = if (arguments.target.id == kord.selfId) {
                    message.respond("Ahem do not try kicking yourself!")
                } else {
                    message.getGuild().kick(arguments.target.id)
                }
                message.respond {
                    embed {
                        title = "Kicking the member"
                        description = "Reason ${arguments.reason} , Member being kicked ${arguments.target.mention} :"
                    }
                }

            }
        }

        slashCommand(::kickSlashArgs) {
            name = "kick"
            description = "Ask the bot to kick a user"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //guild(TEST_SERVER_ID)  // it'll take an hour to show publically

            check { hasPermission(Permission.KickMembers) ; message= "You are missing the required permissions"}


            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@KickCommandH.kord



                // Don't kick ourselves on request, kick the requested user!
                val realTarget = if (arguments.target.id == kord.selfId) {
                    publicFollowUp {
                        content = "Ahem do not try kicking yourself!"
                    }
                } else {
                    arguments.target.kick(reason = arguments.reason )
                }
                publicFollowUp {
                    embed {
                        title = "Kicking the member"
                        description = "Reason ${arguments.reason} , Member being kicked ${arguments.target.mention} :"
                    }
                }

            }
        }
    }

    inner class kickArgs : Arguments() {
        val target by member("target", description = "Person you want to kick")

        val reason by defaultingCoalescingString(
            "reason",

            defaultValue = "Nothing",
            description = "What's the reason you want to kick a person for"
        )
    }

    inner class kickSlashArgs : Arguments() {
        val target by member("target", description = "Person you want to kick")

        // Coalesced strings are not currently supported by slash commands
        val reason by defaultingString(
            "reason",

            defaultValue = "Nothing",
            description = "What's the reason you want to kick a person for"
        )
    }
}
