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
import dev.kord.core.behavior.ban
import dev.kord.rest.builder.message.create.embed

import helia.TEST_SERVER_ID


@OptIn(KordPreview::class)
class BanCommandH : Extension()  {
    override val name = "ban"


    override suspend fun setup() {
        command(::banArgs) {
            name = "ban"
            description = "Ask the bot to ban a user"

            check { hasPermission(Permission.BanMembers); message= "You are missing the required permissions"  }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@BanCommandH.kord

                // Don't ban ourselves on request, ban the requested user!
                val realTarget = if (arguments.target.id == kord.selfId) {
                    message.respond("Ahem do not try banning yourself!")
                } else {

                    arguments.target.ban({
                        reason = arguments.reason
                    })
                }
                message.respond {
                    embed {
                        title = "baning the member"
                        description = "Reason ${arguments.reason} , Member being banned ${arguments.target.mention} :"
                    }
                }

            }
        }

        slashCommand(::banSlashArgs) {
            name = "ban"
            description = "Ask the bot to ban a user"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //guild(TEST_SERVER_ID)  // it'll take an hour to show publically
            check { hasPermission(Permission.BanMembers); message= "You are missing the required permissions" }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@BanCommandH.kord



                // Don't ban ourselves on request, ban the requested user!
                val realTarget = if (arguments.target.id == kord.selfId) {
                    publicFollowUp {
                        content = "Ahem do not try banning yourself!"
                    }
                } else {
                    arguments.target.ban({
                        reason = arguments.reason
                    })
                }
                publicFollowUp {
                    embed {
                        title = "baning the member"
                        description = "Reason ${arguments.reason} , Member being banned ${arguments.target.mention} :"
                    }
                }

            }
        }
    }

    inner class banArgs : Arguments() {
        val target by member("target", description = "Person you want to ban")

        val reason by defaultingCoalescingString(
            "reason",

            defaultValue = "Nothing",
            description = "What's the reason you want to ban a person for"
        )
    }

    inner class banSlashArgs : Arguments() {
        val target by member("target", description = "Person you want to ban")

        // Coalesced strings are not currently supported by slash commands
        val reason by defaultingString(
            "reason",

            defaultValue = "Nothing",
            description = "What's the reason you want to ban a person for"
        )
    }
}