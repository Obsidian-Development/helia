package helia.extensions
import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingCoalescingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.defaultingString
import com.kotlindiscord.kord.extensions.commands.converters.impl.member
import com.kotlindiscord.kord.extensions.commands.converters.impl.user
import com.kotlindiscord.kord.extensions.commands.parser.Arguments
import com.kotlindiscord.kord.extensions.commands.slash.AutoAckType
import com.kotlindiscord.kord.extensions.extensions.Extension
import com.kotlindiscord.kord.extensions.utils.respond
import dev.kord.common.annotation.KordPreview
import dev.kord.core.behavior.ban
import dev.kord.rest.Image
import dev.kord.rest.builder.message.create.embed

import helia.TEST_SERVER_ID


@OptIn(KordPreview::class)
class GuildCommandH : Extension()   {
    override val name = "guild"


    override suspend fun setup() {
        command() {
            name = "guild"
            description = "Show guild information"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@GuildCommandH.kord

                message.respond {
                    embed {
                        title = "Guild Info"
                        description = "Information about guild"
                        field {
                            name = "Server name"
                            value = "```${message.getGuild().name}```"
                            inline = true
                        }
                        field {
                            name = "Server ID"
                            value = "```${message.getGuild().id.value}```"
                            inline = true
                        }
                        field {
                            name = "Owner"
                            value = "```${message.getGuild().owner.asMember().username}```"
                            inline = true
                        }
                        field {
                            name = "Verification Level"
                            value = "```${message.getGuild().verificationLevel.value}```"
                            inline = true
                        }
                        field {
                            name = "Member Count"
                            value = "```${message.getGuild().memberCount}```"
                            inline = true
                        }
                        thumbnail {
                            url = message.getGuild().getIconUrl(format = Image.Format.JPEG).toString()

                        }

                    }
                }

            }
        }

        slashCommand() {
            name = "guild"
            description = "Show guild information"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //guild(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@GuildCommandH.kord

                publicFollowUp {
                    embed {
                        title = "Guild Info"
                        description = "Information about guild"
                        field {
                            name = "Server name"
                            value = "```${guild!!.name}```"
                            inline = true
                        }
                        field {
                            name = "Server ID"
                            value = "```${guild!!.id.value}```"
                            inline = true
                        }
                        field {
                            name = "Owner"
                            value = "```${guild!!.owner.asMember().username}```"
                            inline = true
                        }
                        field {
                            name = "Verification Level"
                            value = "```${guild!!.verificationLevel.value}```"
                            inline = true
                        }
                        field {
                            name = "Member Count"
                            value = "```${guild!!.memberCount}```"
                            inline = true
                        }
                        thumbnail {
                            url = guild!!.getIconUrl(format = Image.Format.JPEG).toString()

                        }

                    }
                }

            }
        }
    }
}