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
import org.codehaus.groovy.ast.expr.Expression
import javax.script.ScriptEngineManager

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
                val e = ScriptEngineManager().getEngineByName("js")
                var expression = ""


                message.respond {
                    embed {
                        title = "Calculator"
                        description = "${expression}"
                        components() {
                            interactiveButton {
                                label = "1"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "1"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "2"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "2"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "3"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "3"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "*"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "*"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "EXIT"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    respond("Button five pressed!")
                                }
                            }
                            interactiveButton {
                                label = "4"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "4"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "5"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "5"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "6"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "6"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "÷"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "/"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "←"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    respond("Button ten pressed!")
                                }
                            }
                            interactiveButton {
                                label = "7"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "7"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "8"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "8"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "9"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "9"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "+"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "+"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "Clear"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    respond("Button fivteen pressed!")
                                }
                            }
                            interactiveButton {
                                label = "00"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "00"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "0"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "0"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "."
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "."
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "-"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "-"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "="
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    var result = e.eval(expression)
                                    var formatedres = result.toString()
                                    respond("${formatedres}")

                                }
                            }
                            interactiveButton {
                                label = "("
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += "("
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = ")"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    expression += ")"
                                    respond("${expression}")
                                }
                            }
                            interactiveButton {
                                label = "π"
                                // Style defaults to `Primary`

                                action { // Easy button actions
                                    respond("Button  pressed!")
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
                val e = ScriptEngineManager().getEngineByName("js")
                var expression = ""


                publicFollowUp {
                    embed {
                        title = "test"
                        description = "test"
                    }
                    components() {
                        interactiveButton {
                            label = "1"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "1"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "2"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "2"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "3"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "3"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "*"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "*"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "EXIT"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                respond("Button five pressed!")
                            }
                        }
                        interactiveButton {
                            label = "4"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "4"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "5"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "5"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "6"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "6"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "÷"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "/"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "←"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                respond("Button ten pressed!")
                            }
                        }
                        interactiveButton {
                            label = "7"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "7"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "8"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "8"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "9"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "9"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "+"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "+"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "Clear"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                respond("Button fivteen pressed!")
                            }
                        }
                        interactiveButton {
                            label = "00"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "00"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "0"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "0"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "."
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "."
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "-"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "-"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "="
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                var result = e.eval(expression)
                                var formatedres = result.toString()
                                respond("${formatedres}")

                            }
                        }
                        interactiveButton {
                            label = "("
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += "("
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = ")"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                expression += ")"
                                respond("${expression}")
                            }
                        }
                        interactiveButton {
                            label = "π"
                            // Style defaults to `Primary`

                            action { // Easy button actions
                                respond("Button  pressed!")
                            }
                        }
                    }
                }

            }
        }
    }
}