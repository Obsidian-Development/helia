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
import dev.kord.core.behavior.MemberBehavior
import dev.kord.core.behavior.ban
import dev.kord.core.entity.Role
import dev.kord.rest.builder.message.create.embed

import helia.TEST_SERVER_ID

@OptIn(KordPreview::class)
class UserinfoCommandH : Extension()   {
    override val name = "userinfo"
    override suspend fun setup() {
        command() {
            name = "userinfo"
            description = "Show user information"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@UserinfoCommandH.kord


                message.respond {
                    embed {
                        title = "Userinfo"
                        description = "Information about user"
                        field {
                            name = "Username"
                            value = "```${message.getAuthorAsMember()?.username}```"
                            inline = true
                        }
                        field {
                            name = "ID"
                            value = "```${message.getAuthorAsMember()?.id?.value}```"
                            inline = true
                        }
                        field {
                            name = "Discriminator"
                            value = "```${message.getAuthorAsMember()?.discriminator}```"
                            inline = true
                        }
                        field {
                            name = "Nickname"
                            value = "```${message.getAuthorAsMember()?.nickname}```"
                            inline = true
                        }
                        field {
                            name = "Presence"
                            value = "```${message.getAuthorAsMember()?.getPresenceOrNull().toString()}```"
                            inline = true
                        }
                        field {
                            name = "Joined at"
                            value = "```${message.getAuthorAsMember()?.joinedAt}```"
                            inline = true
                        }
                        thumbnail {
                            url = message.getAuthorAsMember()?.avatar?.url.toString()
                        }





                    }
                }

            }
        }

        slashCommand() {
            name = "userinfo"
            description = "Show user information"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //guild(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@UserinfoCommandH.kord


                publicFollowUp {


                    embed {
                        title = "Userinfo"
                        description = "Information about user"
                        field {
                            name = "Username"
                            value = "```${member?.asMember()?.username}```"
                            inline = true
                        }
                        field {
                            name = "ID"
                            value = "```${member?.asMember()?.id?.value}```"
                            inline = true
                        }
                        field {
                            name = "Discriminator"
                            value = "```${member?.asMember()?.discriminator}```"
                            inline = true
                        }
                        field {
                            name = "Nickname"
                            value = "```${member?.asMember()?.nickname}```"
                            inline = true
                        }
                        field {
                            name = "Presence"
                            value = "```${member?.asMember()?.getPresenceOrNull().toString()}```"
                            inline = true
                        }
                        field {
                            name = "Joined at"
                            value = "```${member?.asMember()?.joinedAt}```"
                            inline = true
                        }
                        thumbnail {
                            url = member?.asMember()?.avatar?.url.toString()
                        }



                    }
                }

            }
        }
    }
}