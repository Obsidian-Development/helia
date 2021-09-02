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
import dev.kord.rest.builder.message.create.embed

import helia.TEST_SERVER_ID

@OptIn(KordPreview::class)
class InviteCommandH : Extension() {
    override val name = "invite"

    override suspend fun setup() {
        command() {
            name = "invite"
            description = "Show bot invite"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@InviteCommandH.kord

                message.respond {
                    embed {
                        title = "Bot invite links"
                        description = "Here you can see bot invite links"
                        components() {
                            linkButton {
                                label = "Recommended permissions invite"  // You can provide both a label and emoji if you like
                                emoji("🔗")

                                url = "https://discord.com/api/oauth2/authorize?client_id=666304823934844938&permissions=204859462&scope=applications.commands%20bot"
                            }
                            linkButton {
                                label = "Minimal permissions invite"  // You can provide both a label and emoji if you like
                                emoji("🔗")

                                url = "https://discord.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=204557314"
                            }
                        }



                    }
                }

            }
        }

        slashCommand() {
            name = "invite"
            description = "Show bot invite"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //invite(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@InviteCommandH.kord

                publicFollowUp {
                    embed {
                        title = "Bot invite links"
                        description = "Here you can see bot invite links"
                    }
                    components() {
                        linkButton {
                            label = "Recommended permissions invite"  // You can provide both a label and emoji if you like
                            emoji("🔗")

                            url = "https://discord.com/api/oauth2/authorize?client_id=666304823934844938&permissions=204859462&scope=applications.commands%20bot"
                        }
                        linkButton {
                            label = "Minimal permissions invite"  // You can provide both a label and emoji if you like
                            emoji("🔗")

                            url = "https://discord.com/oauth2/authorize?client_id=666304823934844938&scope=bot&permissions=204557314"
                        }
                    }
                }

            }
        }
    }
}