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
import dev.kord.common.entity.ButtonStyle
import dev.kord.core.behavior.edit
import dev.kord.core.behavior.ban
import dev.kord.core.behavior.interaction.edit
import dev.kord.core.entity.Message
import dev.kord.core.entity.interaction.PublicFollowupMessage
import dev.kord.rest.builder.message.create.embed
import dev.kord.rest.builder.message.modify.embed


import helia.TEST_SERVER_ID

import org.codehaus.groovy.ast.expr.Expression
import javax.script.ScriptEngineManager

@OptIn(KordPreview::class)
class PurgeCommandH : Extension()   {
    override val name = "purge"
    override suspend fun setup() {
        command() {
            name = "purge"
            description = "Clear an ammount of messages"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@PurgeCommandH.kord
                lateinit var createmessage : Message


                createmessage = message.respond {
                    embed {
                        title = "Purge command"
                        description = "Do you want to purge {placeholder} messages?"
                        components() {
                            interactiveButton {
                                label = "✓"
                                style = ButtonStyle.Success
                                deferredAck = true

                                action { // Easy button actions
                                    createmessage.edit{
                                        this.embed {
                                            title = "Action Complete"
                                            description = "```Purged Messages```"
                                        }
                                        components = mutableListOf()

                                    }
                                }
                            }
                            interactiveButton {
                                label = "X"
                                style = ButtonStyle.Danger
                                deferredAck = true

                                action { // Easy button actions
                                    createmessage.edit{
                                        this.embed {
                                            title = "Action Aborted"
                                            description = "```The action was aborted due to refusal action```"

                                        }
                                    }
                                }
                            }
                        }

                    }
                }

            }
        }

        slashCommand() {
            name = "purge"
            description = "Clear an ammount of messages"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //guild(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@PurgeCommandH.kord
                lateinit var myResponse: PublicFollowupMessage

                myResponse = publicFollowUp {
                    embed {
                        title = "Purge command"
                        description = "Do you want to purge {placeholder} messages?"
                    }
                    components() {
                        interactiveButton {
                            label = "✓"
                            style = ButtonStyle.Success
                            deferredAck = true

                            action { // Easy button actions
                                myResponse.edit{
                                    this.embed {
                                        title = "Action Complete"
                                        description = "```Purged Messages```"
                                    }
                                    components = mutableListOf()
                                }
                            }
                        }
                        interactiveButton {
                            label = "X"
                            style = ButtonStyle.Danger
                            deferredAck = true

                            action { // Easy button actions
                                myResponse.edit{
                                    this.embed {
                                        title = "Action Aborted"
                                        description = "```The action was aborted due to refusal action```"
                                    }
                                    components = mutableListOf()
                                }
                            }
                        }
                    }
                }

            }
        }
    }
}