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
class CalculatorCommandH : Extension()   {
    override val name = "calculator"
    override suspend fun setup() {
        command() {
            name = "calculator"
            description = "Calculator command"

            check { failIf(event.message.author == null) }

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@CalculatorCommandH.kord

                message.respond {
                    embed {
                        title = "test"
                        description = "test"
                        components() {
                            interactiveButton {
                                label = "test"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    respond("Button one pressed!")
                                }
                            }
                            interactiveButton {
                                label = "testt"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    respond("Button two pressed!")
                                }
                            }
                        }


                    }
                }

            }
        }

        slashCommand() {
            name = "calculator"
            description = "Calculator command"

            // We want to send a public follow-up - KordEx will handle the rest
            autoAck = AutoAckType.PUBLIC

            //invite(TEST_SERVER_ID)  // it'll take an hour to show publically

            action {
                // Because of the DslMarker annotation KordEx uses, we need to grab Kord explicitly
                val kord = this@CalculatorCommandH.kord

                publicFollowUp {
                    embed {
                        title = "test"
                        description = "test"
                    }
                    components() {
                        interactiveButton {
                            label = "test"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                respond("Button one pressed!")
                            }
                        }
                        interactiveButton {
                            label = "testt"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                respond("Button two pressed!")
                            }
                        }
                    }
                }

            }
        }
    }
}